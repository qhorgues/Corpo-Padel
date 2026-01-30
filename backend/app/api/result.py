from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func

from app.database import get_db
from app.api.deps import get_current_user
from app.models.models import Match, Team
from app.schemas.result import MyResultsResponse, ResultItemResponse, OpponentsResponse, StatisticsResponse
from app.schemas.ranking import RankingsResponse, RankingItemResponse

router = APIRouter()


@router.get("/my-results", response_model=MyResultsResponse)
def my_results(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    This function returns the results of the connected user.

    param : db - The session of database.
    param : current_user - The client.
    return : Return the results and statistics.
    """

    player = current_user.player
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found"
        )

    matches = db.query(Match).filter(
        and_(or_(
                Match.team1.has(player1_id=player.id),
                Match.team1.has(player2_id=player.id),
                Match.team2.has(player1_id=player.id),
                Match.team2.has(player2_id=player.id),
            ),
            Match.status == "TERMINE"
        )
    ).all()

    results = []
    wins = 0
    losses = 0

    for match in matches:
        if match.team1.player1_id == player.id or match.team1.player2_id == player.id:
            opponent_team = match.team2
            player_score = match.score_team1
            opp_score = match.score_team2
        else:
            opponent_team = match.team1
            player_score = match.score_team2
            opp_score = match.score_team1

        score = f"{player_score}-{opp_score}" if player_score is not None and opp_score is not None else None

        if player_score is not None and opp_score is not None:
            if player_score > opp_score:
                result_text = "VICTOIRE"
                wins += 1
            elif player_score < opp_score:
                result_text = "DEFAITE"
                losses += 1
            else:
                result_text = "NUL"
        else:
            result_text = "A_VENIR"

        opp_players = [
            f"{opponent_team.player1.first_name} {opponent_team.player1.last_name}",
            f"{opponent_team.player2.first_name} {opponent_team.player2.last_name}",
        ]

        opponents = OpponentsResponse(
            company=opponent_team.company,
            players=opp_players
        )

        results.append(ResultItemResponse(
            match_id=match.id,
            date=match.event.event_date,
            opponents=opponents,
            score=score,
            result=result_text,
            court_number=match.court_number
        ))

    total_matches = len(results)
    win_rate = (wins / total_matches) * 100 if total_matches > 0 else 0

    statistics = StatisticsResponse(
        total_matches=total_matches,
        wins=wins,
        losses=losses,
        win_rate=win_rate
    )

    return MyResultsResponse(results=results, statistics=statistics)



@router.get("/rankings", response_model=RankingsResponse)
def rankings(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    This function returns the global ranking of companies.

    param : db - The session of database.
    param : current_user - The client.
    return : Return rankings.
    """

    matches = db.query(Match).filter(Match.status == "TERMINE").all()

    stats = {}

    for m in matches:
        t1 = m.team1
        t2 = m.team2

        if t1.company not in stats:
            stats[t1.company] = {"matches": 0, "wins": 0, "losses": 0, "sets_won": 0, "sets_lost": 0}
        if t2.company not in stats:
            stats[t2.company] = {"matches": 0, "wins": 0, "losses": 0, "sets_won": 0, "sets_lost": 0}

        stats[t1.company]["matches"] += 1
        stats[t2.company]["matches"] += 1

        stats[t1.company]["sets_won"] += m.score_team1 or 0
        stats[t1.company]["sets_lost"] += m.score_team2 or 0
        stats[t2.company]["sets_won"] += m.score_team2 or 0
        stats[t2.company]["sets_lost"] += m.score_team1 or 0

        if (m.score_team1 or 0) > (m.score_team2 or 0):
            stats[t1.company]["wins"] += 1
            stats[t2.company]["losses"] += 1
        elif (m.score_team2 or 0) > (m.score_team1 or 0):
            stats[t2.company]["wins"] += 1
            stats[t1.company]["losses"] += 1

    ranking_list = []
    for company, v in stats.items():
        points = v["wins"] * 3
        ranking_list.append({
            "company": company,
            "matches_played": v["matches"],
            "wins": v["wins"],
            "losses": v["losses"],
            "points": points,
            "sets_won": v["sets_won"],
            "sets_lost": v["sets_lost"],
        })

    ranking_list.sort(key=lambda x: x["points"], reverse=True)

    for idx, item in enumerate(ranking_list, start=1):
        item["position"] = idx

    return RankingsResponse(rankings=[RankingItemResponse(**r) for r in ranking_list])
