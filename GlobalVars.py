#!/usr/bin/env python3

#Class containing the challenge and a list of things it excludes
class ChallengeComponent:
    def __init__(self, goal, ctype, excl):
        self.goal = goal
        self.ctype = ctype
        self.excl = excl

class Map:
    def __init__(self, id, title, weapons, floors, unique_npcs, civilians, unique_disguises, npc_outfits):
        self.id = id
        self.title = title
        self.weapons = weapons
        self.floors = floors
        self.unique_npcs = unique_npcs
        self.civilians = civilians
        self.unique_disguises = unique_disguises
        self.npc_outfits = npc_outfits

class FinalChallengeComponent:
    def __init__(self, title, line1, line2):
        self.title = title
        self.line1 = line1
        self.line2 = line2

mainChallenges = []
extraChallenges = []
selected = []
excluded = []
map = None
targetCount = 5
npc_types_list = ["civilian","armed","unique"]

finalChallenge = []

