from rps.main import Play, Outcome

def logic(p1_choice:Play, p2_choice:Play):
    if p1_choice == p2_choice:
        return Outcome.draw

    elif p1_choice == Play.rock:
        return Outcome.win if p2_choice == Play.scissors else Outcome.loss

    elif p1_choice == Play.paper:
        return Outcome.win if p2_choice == Play.rock else Outcome.loss

    elif p1_choice == Play.scissors:
        return Outcome.win if p2_choice == Play.paper else Outcome.loss