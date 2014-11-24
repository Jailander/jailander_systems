# Announcing achievements

## Twitter

If you want to tweet your announcements, you must have the `tweets.py` node running from `strands_tweets`. This is detailed in its [README](https://github.com/strands-project/strands_utils/blob/master/strands_tweets/README.md).

## Usage

You first need to create a file with your target achievements. there is an example in the support dir

```
rosrun marathon_achievements achievement_monitor.py achievements.yaml
```

Finally run the monitor node must be running for this to work
```
rosrun marathon_reporter mileage_monitor.py
```

## Defining Achievements

Achievements are defined using a yaml file like the following please put the values in ascending order

```yaml
achievements:
  <achievemment_type>: 
  - {val: 0, achievement: "I got to 0"}
  - {val: 1, achievement: "I to to 1"}
    <achievemment_type>: 
  - {val: 1000, achievement: "I got 1000 in something else"}
```
e.g.
```yaml
achievements:
  run_duration: 
  - {val: 0, achievement: "Let's get cracking"}
  - {val: 1, achievement: "I've run for an hour"}
  - {val: 10, achievement: "I've run for ten hours"}
  - {val: 24, achievement: "I've run a whole day"}
  distance:
  - {val: 1000, achievement: "I've run for one kilometre"}
  - {val: 10000, achievement: "I've run for ten kilometres"}
  - {val: 42195, achievement: "I've just completed an actual marathon."}
  - {val: 100000, achievement: "I've run for one hundred kilometres"}
```
There are two types of value for `<achievemment_type>`. If it is either `run_duration` or `distance` then the `val` argument is interpreted as hours or kilometres respectively. 
