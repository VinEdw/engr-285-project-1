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

#py_script("default_parameters", put_output: false, put_fname: true)

#py_script("measure_outcome_chances", put_output: false, put_fname: true)

#let outcome_chance_test(attribute) =  {
  py_script("test_" + attribute, put_output: false)
  figure(
    image("media/outcome_chances_" + attribute + ".svg", width: 80%),
    caption: [Outcome Chances vs #raw(attribute)],
  )
}

== `breed_time`

#outcome_chance_test("breed_time")

== `energy_gain`

#outcome_chance_test("energy_gain")

== `breed_energy`

#outcome_chance_test("breed_energy")

== `side_length`

#outcome_chance_test("side_length")

== `aspect_ratio`

#outcome_chance_test("aspect_ratio")

== `initial_fish`

#outcome_chance_test("initial_fish")

== `initial_sharks`

#outcome_chance_test("initial_sharks")

== `start_energy`

#outcome_chance_test("start_energy")


= Main Simulation Parameters

#py_script("measure_ratios", put_output: false, put_fname: true)

#let lvm_ratios_test(attribute) =  {
  py_script("test_" + attribute + "_ratios", put_output: false)
  figure(
    image("media/lvm_ratios_" + attribute + ".svg", width: 90%),
    caption: [LVM Ratios vs #raw(attribute)],
  )
}

== `breed_time`

#lvm_ratios_test("breed_time")

== `energy_gain`

#lvm_ratios_test("energy_gain")

== `breed_energy`

#lvm_ratios_test("breed_energy")

= Circular Initialization

#let outcome_chance_test_circular(attribute) =  {
  py_script("test_" + attribute, put_output: false)
  figure(
    image("media/outcome_chances_" + attribute + "_circular.svg", width: 80%),
    caption: [Outcome Chances vs #raw(attribute) (Circular Initialization)],
  )
}

== `breed_time`

#outcome_chance_test_circular("breed_time")

== `energy_gain`

#outcome_chance_test_circular("energy_gain")

== `breed_energy`

#outcome_chance_test_circular("breed_energy")

== `side_length`

#outcome_chance_test_circular("side_length")

== `aspect_ratio`

#outcome_chance_test_circular("aspect_ratio")

== `initial_fish`

#outcome_chance_test_circular("initial_fish")

== `initial_sharks`

#outcome_chance_test_circular("initial_sharks")

== `start_energy`

#outcome_chance_test_circular("start_energy")


= Extension

