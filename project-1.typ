#import "engr-conf.typ": conf, py_script
#show: conf.with(
  title: [Study of Predator-Prey Dynamics],
  authors: (
    (first_name: "Vincent", last_name: "Edwards"),
    (first_name: "Julia", last_name: "Corrales"),
    (first_name: "Rachel", last_name: "Gossard"),
  ),
  date: datetime(year: 2025, month: 4, day: 13),
)

= Lotka-Volterra Model (LVM)

The Lotka-Volterra Model (LVM) models the dynamics between a predator species ($y$) and a prey species ($x$) over time ($t$).
$
(d y)/(d t) = -a y + b x y quad (d x) / (d t) = +d x - c y x
$
The model depends on four parameters.
- $a$: decay rate of the predators
- $b$: proportionality for how predators grow due to eating prey
- $c$: proportionality for how prey decay due to being eaten by predators
- $d$: growth rate of the prey

Dividing the differential equations by each other yields $(d y)/(d x)$.
$
(d y)/(d x) = b/c (y(x - a/b)) / (x(d/c - y))
$
Since this equation does not depend explicitly on time, it can be used to create phase portraits.
The solutions swirl counter-clockwise around $x = a/b$ and $y = d/c$.

= Types of Simulation Outcomes

= Conditions for Good Modeling

= Main Simulation Parameters

== `breed_time`

== `energy_gain`

== `breed_energy`

= Circular Initialization

= Extension

