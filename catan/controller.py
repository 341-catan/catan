from database import db_session
from models import *
from string import replace

import vertices
import json

def get_log(gameid, sequence):
    g= Game.query.get(gameid)
    log = [i.Action for i in Log.query.filter(Log.GameID == gameid).filter(Log.Sequence >= sequence).all()]
    return (g.NextSequence, "[" + ",".join(log) + "]")

"""
add_log takes an object, adds the log beside it, and returns the whole thing as JSON

It uses a DIRTY DIRTY HACK.
"""
def add_log(obj, gameid, sequence):
    log = get_log(gameid, sequence)

    #A dirty dirty hack that prevents us from having to parse and serialize the JSON all over again
    flagged = json.dumps({ "response": obj, "sequence": Game.query.get(gameid).NextSequence, "log": "REPLACE_TOKEN"});
    return flagged.replace('"REPLACE_TOKEN"', log, 1)

def create_game(userid):
    g = Game()

    db_session.add(g);
    db_session.commit()
    return g.GameID

def start_game(gameid, sequence):
    g = Game.query.get(gameid);

    g.start();
    g.log({ "action" : "hexes_placed", "args": [i.json() for i in g.hexes]})

    db_session.commit()

    return "success"

def build_settlement(gameid, userid, vertex, sequence):
    p = decompress(vertex)
    if isvalid(p): #TODO: we also need to figure out whether the game logic allows it
        g = Game.query.get(id)

        s = Settlement(vertex, userid, Settlement.TOWN)
        g.settlements.append(s)
        g.log({ "action" : "settlement_built", "args" : [userid, vertex]})

        db_session.commit()

        return "success"
    else:
        return "failure"

"""
def upgrade_settlement():
def development_card():
def build_road():
def move_robber():
def discard_cards():
"""