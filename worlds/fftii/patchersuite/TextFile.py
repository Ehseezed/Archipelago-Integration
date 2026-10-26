from ..data.text import text_id_lookup, text_data_lookup


def apply_string_table(table: list[str]) -> bytearray:
    result = bytearray()
    for string in table:
        i: int = 0
        while i < len(string):
            character = string[i]
            if character == "{":
                if string[i + 1] == "C":
                    bytes_to_write = text_data_lookup[string[i:i + 11]].id.to_bytes(2)
                    result.extend(bytes_to_write)
                    i += 11
                    continue
                elif string[i + 1] == "Z":
                    bytes_to_write = text_data_lookup[string[i:i + 4]].id.to_bytes(2)
                    result.extend(bytes_to_write)
                    i += 4
                    continue
                else:
                    byte_to_write = text_data_lookup[string[i:i + 4]].id
                    i += 4
            elif character == "-":
                result.extend([0xD1, 0x1D])
                i += 1
                continue
            elif character == ",":
                result.extend([0xDA, 0x74])
                i += 1
                continue
            elif character == " ":
                result.extend([0xDA, 0x73])
                i += 1
                continue
            else:
                byte_to_write = text_data_lookup[character].id
                i += 1
            try:
                result.append(byte_to_write)
            except ValueError:
                raise ValueError(character + " not found for string table.")
        result.append(0xFE)
    return result


class TextFile:
    all_data: bytearray

    def init_string_list(self, working_data: bytearray, count: int):
        return_list = list()
        working_string = ""
        return_data = working_data.copy()
        i = 0
        while len(return_list) < count:
            if (0xD1 <= working_data[i] <= 0xDA) or working_data[i] == 0xE3:
                lookup = (working_data[i] << 8) + working_data[i + 1]
                try:
                    working_string += text_id_lookup[lookup]
                except:
                    # raise
                    working_string += "?"
                i += 1
            elif working_data[i] == 0xFE:
                return_list.append(working_string)
                working_string = ""
            else:
                try:
                    working_string += text_id_lookup[working_data[i]]
                except KeyError:
                    #raise
                    working_string += "?"
            i += 1
        return return_list, return_data, i

    def test_bytes(self, data_to_test: bytearray, offset: int):
        for i in range(len(data_to_test)):
            assert data_to_test[i] == self.all_data[offset + i], (i, data_to_test[i])