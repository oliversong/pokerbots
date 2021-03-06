#ACTIONS
BET = 0#"BET"
CALL = 1#"CALL"
CHECK = 2#"CHECK"
RAISE = 3#"RAISE"
FOLD = 4#"FOLD"
DEAL = 5#"DEAL"
POST = 6#"POST"
REFUND = 7#"REFUND"
SHOW = 8#"SHOW"
TIE = 9#"TIE"
WIN = 10#"WIN"

ACTION_TYPES = ["BET", "CALL", "CHECK", "RAISE", "FOLD", "DEAL", "POST",
                "REFUND", "SHOWS", "TIE", "WIN"]

#STREETS
PREFLOP = 0
FLOP = 1
TURN = 2
RIVER = 3

STREET_TYPES = ["PREFLOP","FLOP","TURN","RIVER"]

#PACKET TYPES
NEWGAME = "NEWGAME"
NEWHAND = "NEWHAND"
GETACTION = "GETACTION"
HANDOVER = "HANDOVER"

#ACTION AMOUNT TYPES
POTAMOUNT = "POT AMOUNT"
BETAMOUNT = "BET AMOUNT"
ABSAMOUNT = "ABS AMOUNT"

#PLAYER INDICES
ME = 0
LEFTOPP = 1
RIGHTOPP = 2

ITERATIONS = 10000

#EV COMPARISONS
AWFUL = 0
BAD = 1
OK = 2
GOOD = 3
UNKNOWN = -1

#BET/RAISE BINS
BIN1 = 0
BIN2 = 1
BIN3 = 2
BIN4 = 3
