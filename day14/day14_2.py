#!/usr/bin/env python3
# Imports
from math import ceil, inf
from collections import defaultdict, namedtuple
from typing import List

from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2019, day=14)
puzzle_input = puzzle.get_input()
# puzzle_input = [
#     "10 ORE => 10 A",
#     "1 ORE => 1 B",
#     "7 A, 1 B => 1 C",
#     "7 A, 1 C => 1 D",
#     "7 A, 1 D => 1 E",
#     "7 A, 1 E => 1 FUEL",
# ] #31
# puzzle_input = [
#     "9 ORE => 2 A",
#     "8 ORE => 3 B",
#     "7 ORE => 5 C",
#     "3 A, 4 B => 1 AB",
#     "5 B, 7 C => 1 BC",
#     "4 C, 1 A => 1 CA",
#     "2 AB, 3 BC, 4 CA => 1 FUEL",
# ] #165
# puzzle_input = [
#     "157 ORE => 5 NZVS",
#     "165 ORE => 6 DCFZ",
#     "44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL",
#     "12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ",
#     "179 ORE => 7 PSHF",
#     "177 ORE => 5 HKGWZ",
#     "7 DCFZ, 7 PSHF => 2 XJWVT",
#     "165 ORE => 2 GPVTF",
#     "3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT",
# ] # 13312
# puzzle_input = [
#     "2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG",
#     "17 NVRVD, 3 JNWZP => 8 VPVL",
#     "53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL",
#     "22 VJHF, 37 MNCFX => 5 FWMGM",
#     "139 ORE => 4 NVRVD",
#     "144 ORE => 7 JNWZP",
#     "5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC",
#     "5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV",
#     "145 ORE => 6 MNCFX",
#     "1 NVRVD => 8 CXFTF",
#     "1 VJHF, 6 MNCFX => 4 RFSQX",
#     "176 ORE => 6 VJHF",
# ] #180697
# puzzle_input = [
#     "171 ORE => 8 CNZTR",
#     "7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL",
#     "114 ORE => 4 BHXH",
#     "14 VRPVC => 6 BMBT",
#     "6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL",
#     "6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT",
#     "15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW",
#     "13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW",
#     "5 BMBT => 4 WPTQ",
#     "189 ORE => 9 KTJDG",
#     "1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP",
#     "12 VRPVC, 27 CNZTR => 2 XDBXC",
#     "15 KTJDG, 12 BHXH => 5 XCVML",
#     "3 BHXH, 2 VRPVC => 7 MZWV",
#     "121 ORE => 7 VRPVC",
#     "7 XCVML => 6 RJRHP",
#     "5 BHXH, 4 VRPVC => 5 LTCX",
# ] # 2210736
class Reaction(object):
    def __init__(self, produced: dict, consumed: dict) -> None:
        self.produced = produced
        self.consumed = consumed

    def __repr__(self):
        return "Reaction(" + ", ".join([f"{num} {item}" for item, num in self.consumed.items()]) + " => " + ", ".join([f"{num} {item}" for item, num in self.produced.items()]) + ")"

    def balance(self, multiplier):
        self.produced = {p: n*multiplier for p, n in self.produced.items()}
        self.consumed = {c: n*multiplier for c, n in self.produced.items()}
    
    def produces(self, item):
        return item in self.produced
    
    def consumes(self, item):
        return item in self.consumed

    @staticmethod
    def parse_reaction(line:str) -> 'Reaction':
        produced = {}
        consumed = {}
        is_consuming = True
        for item in line.split(","):
            item = item.strip()
            if is_consuming:
                if "=>" not in item:
                    item = item.split(" ")
                    assert item[1] not in consumed
                    consumed[item[1]] = int(item[0])
                else:
                    consumed_item, produced_item = item.split("=>")
                    consumed_item = consumed_item.strip().split(" ")
                    produced_item = produced_item.strip().split(" ")
                    assert consumed_item[1] not in consumed
                    consumed[consumed_item[1]] = int(consumed_item[0])
                    assert produced_item[1] not in produced
                    produced[produced_item[1]] = int(produced_item[0])
                    is_consuming = False
            else:
                item = item.split(" ")
                assert item[1] not in produced
                produced[item[1]] = int(item[0])
        return Reaction(produced=produced, consumed=consumed)
            

# Actual Code
class ReactionGraph(object):
    Relation = namedtuple("Relation", ("item","produced", "consumed"))
    Element = namedtuple("Element", ("item","amount"))
    def __init__(self, reactions):
        self.relations = ReactionGraph.build_relations(reactions)
        self.order = defaultdict(int)
        self.reaction_index = {}
        for reaction in reactions:
            for produced_item in reaction.produced:
                self.reaction_index[produced_item] = reaction

    @staticmethod
    def build_relations(reactions: List[Reaction]):
        relations = defaultdict(set)
        for reaction in reactions:
            for produced_item, amount_produced in reaction.produced.items():
                for consumed_item, amount_consumed in reaction.consumed.items():
                    relations[produced_item].add(ReactionGraph.Relation(item=consumed_item, produced=amount_produced, consumed=amount_consumed))
        return relations
    
    def order_elements(self, start="FUEL"):
        curr_wave = [start]
        order = 0
        while curr_wave:
            new_wave = []
            for elem in curr_wave:
                for relation in self.relations[elem]:
                    self.order[relation.item] = order
                    new_wave.append(relation.item)
            curr_wave = new_wave
            order += 1

    def create_fuel(self, amount=1):
        required = {}
        curr_wave = defaultdict(int)
        curr_wave["FUEL"] = amount
        while curr_wave:
            next_elem = min(curr_wave, key=lambda e: self.order[e])
            amount_required = curr_wave.pop(next_elem)
            if next_elem not in self.reaction_index:
                required[next_elem] = amount_required
                continue
            # Create this element
            reaction = self.reaction_index[next_elem]
            amount_produced = reaction.produced[next_elem]
            multiple = ceil(amount_required/amount_produced)
            for consumed_item, amount in reaction.consumed.items():
                curr_wave[consumed_item] += multiple*amount
        return required


# First create a graph of which elements depend on which other elements
reactions = list(map(Reaction.parse_reaction, puzzle_input))
reaction_graph = ReactionGraph(reactions)
reaction_graph.order_elements()
AVAILABLE_ORE = 1000000000000
done = False
lower_bound, upper_bound = 1, AVAILABLE_ORE
while upper_bound - lower_bound > 1:
    mid = (upper_bound + lower_bound) // 2
    requirements = reaction_graph.create_fuel(amount=mid)
    assert len(requirements) == 1 and "ORE" in requirements
    required_ore = requirements["ORE"]
    if required_ore > AVAILABLE_ORE:
        upper_bound = mid
    elif required_ore < AVAILABLE_ORE:
        lower_bound = mid
    else:
        break
print(lower_bound)  