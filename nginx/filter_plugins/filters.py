#!/usr/bin/python

from typing import Dict, List

from ansible.errors import AnsibleFilterError, AnsibleFilterTypeError


class FilterModule(object):
    def filters(self):
        return {
            'rename_keys': self.rename_keys
        }
    
    def rename_keys(self, dict: Dict, mappings: List) -> Dict:
        if not isinstance(dict, Dict):
            raise AnsibleFilterTypeError("input must be a map")

        result = {}
        for mapping in mappings:
            if not len(mapping) == 2:
                raise AnsibleFilterError("mapping must be a list of string-tuples")
            key = mapping[0]
            target = mapping[1]
            try:
                result[target] = dict[key]
            except KeyError:
                pass
        keys = [item for sublist in mappings for item in sublist]
        for item in dict.items():
            if item[0] not in keys:
                result[item[0]] = item[1]
        
        return result