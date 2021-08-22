from rps.main import Play, Outcome

def logic(p1:Play, p2:Play):
    if p1 == p2:
        return Outcome.draw

    elif p1 == Play.rock:
        return Outcome.win if p2 == Play.scissors else Outcome.loss

    elif p1 == Play.paper:
        return Outcome.win if p2 == Play.rock else Outcome.loss

    elif p1 == Play.scissors:
        return Outcome.win if p2 == Play.paper else Outcome.loss