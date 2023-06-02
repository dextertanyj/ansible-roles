#!/usr/bin/python

from copy import deepcopy
from numbers import Number
from typing import Dict, List

from ansible.errors import AnsibleFilterError, AnsibleFilterTypeError


class FilterModule(object):
    def filters(self):
        return {
            'flatten_rules': self.flatten_rules
        }
    
    def flatten_rules(self, rules: List, properties: List, allow_primative=True, allow_empty=True) -> List[Dict]:
        if not isinstance(rules, list):
            raise AnsibleFilterTypeError("input must be a list")
        if not isinstance(properties, list):
            raise AnsibleFilterTypeError("properties must be a list of strings")
        
        results = rules

        def extract_field(rule: Dict, field: List, allow_primative: bool, allow_empty: bool) -> List[Dict]:
            results: List[Dict] = []
            if not isinstance(rule, dict):
                raise AnsibleFilterTypeError("input must be a list of maps")
            try:
                values = rule[field]
            except KeyError:
                if allow_empty:
                    return [rule]
                raise AnsibleFilterError(f"could not find {field} in rule: ({rule})")
            if isinstance(values, str) or isinstance(values, Number) and allow_primative:
                return [rule]
            if not isinstance(values, list):
                raise AnsibleFilterError(f"the key {field} should point to a list")
            
            for value in values:
                copy = deepcopy(rule)
                copy[field] = value
                results.append(copy)
            return results
            
        for field in properties:
            extracted = []
            for rule in results:
                extracted.extend(extract_field(rule, field, allow_primative, allow_empty))
            results = extracted

        return results
