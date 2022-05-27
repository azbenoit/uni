#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 10:29:09 2021

@author: alixb1908
"""

class Vote:
    """A single vote object.
    
    Data attributes:
    - preference_list: a list of the preferred parties for this voter,
      in descending order of preference.
    """
    def __init__(self, preference_list):
        self.preference_list = preference_list
        
    def __str__(self):
        
        if self.preference_list == []:
            return 'Blank'
        else:
            ret = self.preference_list[0]
            for p in self.preference_list[1:]:
                ret += f' > {p}'
            return ret
        
    def __repr__(self):
        return f'Vote({self.preference_list})'
    def first_preference(self):
        if(self.preference_list == []):
            return None
        else:
            return self.preference_list[0]
        
    def preference(self, names):
        """Return the item in names that occurs first in the preference list,
        or None if no item in names appears.
        """
        for p in self.preference_list:
            if p in names:
                return p
        else: return None
        
        
        
        
class Election:
    """A basic election class.
    
    Data attributes:
    - parties: a list of party names
    - blank: a list of blank votes
    - piles: a dictionary with party names for keys
      and lists of votes (allocated to the parties) for values
    - dead: dead votes
    """
    
    def __init__(self, parties):
        self.parties = parties
        self.blank = []
        self.piles = {name:[] for name in self.parties}
        self.dead = []
    
    def add_vote(self, vote):
        """Append the vote to the corresponding pile."""
        p = vote.first_preference()
        if p == None:
            self.blank.append(vote)
        else:
            self.piles[p].append(vote)
        
        

    def status(self):
        """Return the current status of the election:
        a dictionary mapping each of the party names in the piles
        to the number of votes in their pile.
        """
        d = {}
        for p in self.piles:
            d[p] = len(self.piles[p])
        return d
    
    def add_votes_from_file(self, filename):
        """
        Convert each line of the file into a Vote,
        and append each of the votes to the correct pile.
        """
        with open(filename, 'r')as f:
            lines = f.readlines()
            for l in lines:
                l = l[:len(l)-1]
                l = l.strip()
# =============================================================================
#                 print(repr(l))
# =============================================================================
                if l == '':
                    vote = []
                else:
                    vote = l.split(' ')
                v = Vote(vote)
# =============================================================================
#                 print(v)
# =============================================================================
                self.add_vote(v)

    def first_past_the_post_winner(self):
        """Return the winner of this election under
        the first-past-the-post system, or None if
        the election is tied.
        """
        stat = self.status()
        l = []
        for p in self.parties:
            l.append(stat[p])
        maxv = max(l)
        i = l.index(maxv)
        count = 0
        for n in l:
            if n == maxv: count+=1
        if count == 1:
            return self.parties[i]
        else:
            return None
        
    def weighted_status(self):
        """Returns a dictionary with keys being the parties
        and values being the number of points (counted using
        the weighted scheme) that the party got.
        """
        d = {}
        for p in self.parties:
            d[p] = 0
        for p in self.piles:
            for v in self.piles[p]:
                for i in range(len(v.preference_list)):
                    d[v.preference_list[i]] += 5 - i
        return d

    def weighted_winner(self):
        """
        Return the winner of this election under
        the weighted voting scheme.
        """
        stat = self.weighted_status()
        l = []
        winners = []
        for p in self.parties:
            l.append(stat[p])
        maxv = max(l)
        for i in range(len(l)): 
            if l[i] == maxv:
                winners.append(self.parties[i])
        winners.sort()
        return winners[0]
        
                
    def eliminate(self, party):
        """Remove the given party from piles, and redistribute its 
        votes among the parties not yet eliminated, according to 
        their preferences.  If all preferences have been eliminated, 
        then add the vote to the dead list.
        """
        to_redistribute = self.piles.pop(party)
        for vote in to_redistribute:
             pref = vote.preference(list(self.piles.keys()))
             if pref == None:
                 self.dead.append(vote)    
             else:
                 self.piles[pref].append(vote)
    
    def round_loser(self):
        """Return the name of the party to be eliminated from the next round."""
        stat = self.status()
        minval = min(list(stat.values()))
        count = 0
        loosers = []
        for p in stat:
            if stat[p] == minval:
                count+=1
                loosers.append(p)
        fprefs = {}
        for l in loosers:
            fprefs[l] = 0
            for v in self.piles[l]:
                if v.first_preference() == l:
                    fprefs[l] += 1
        minval2 = min(list(fprefs.values()))
        big_ls = []
        for l in loosers:
            if fprefs[l] == minval2:
                big_ls.append(l)
        big_ls.sort()
        return big_ls[0]
            
                
        
            
    def preferential_winner(self):
        """Run a preferential election based on the current piles of votes,
        and return the winning party.
        """
        while len(self.piles) > 1:
            self.eliminate(self.round_loser())
        return list(self.piles.keys())[0]
            


























