# Covers: Expert picks crawler

## 3 types of items

- ScoreItem: for matchup, scores and closing lines
- ExperpickItem: counts for experts' picks
- CoverspickItem: descriptions for individual expert status and pick

## multiple collections joint

1. simple joint with ScoreItem and ExpertpickItem

This is the basic analysis based on summaried counts for expert pick and scores, i.e. not going for the details about individual expert ranking and performance.

``` javascript
db.ScoreItem.aggregate([
{
 $lookup:{
  from: "ExpertpickItem",
  localField: "game_string",
  foreignField: "game_string",
  as: "joint_with_expertpickitem"
 }
}
])

```
