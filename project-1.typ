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

#image("media/thumbnail.png")

// Table of contents
#pagebreak()
#outline()
#pagebreak()

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

The simulation has three main types of outcomes:

+ Both species go extinct
+ Sharks go extinct
+ Neither species goes extinct within steps simulated for

The first outcome occurs when the sharks eat all the fish.
The surviving sharks, now left with no food, subsequently die out.
The second outcome occurs when the sharks eat all the fish nearby, but some fish still remain further away.
The sharks cannot reach those further fish before dying out.
This leaves the fish population unchecked, allowing them to grow until they fill the board.
The third outcome occurs when the simulation does not terminate early, as happens with the other two outcomes, and runs for the full amount of steps specified.
The predator and prey populations oscillate in accord with the Lotka-Volterra model.

Note that the LVM only predicts that the first outcome will only occur if the prey population starts at 0, and the second outcome will only occur if the shark population starts at 0.
But, due to the randomness of the simulation and its discrete nature, these outcomes still occur.
In order to reduce the chances of those extinction outcomes, a relatively large board (`dims = (80, 90)`) was used.
This allows for more fish and shark clusters to form, reducing the chances that the sharks eat _all_ the food in the world.
It also increases the chances that another fish cluster is nearby after the sharks finish devouring one.
In addition, a larger board allows for larger populations and more creature interactions, helping the simulation be a closer approximation of continuous populations and time (the requirements of any differential model).

The graphs in @conditions_for_good_modeling depict how common each of these outcomes are, at least for the sets of parameter tested.
As discussed in the last paragraph, utilizing a large board greatly boosted the chance of neither species going extinct.
Certain parameter modifications increase the chances of extinction (at the expense of the chance of neither going extinct).

= Conditions for Good Modeling <conditions_for_good_modeling>

In order to test the conditions under which it appears the LVM models the simulation results well, tests were run plotting the measured chances of the three main types outcomes (Both Extinct, Sharks Extinct, & Neither Extinct) as each simulation parameter was varied one at a time.
It was reasoned that by examining how the simulation responds to changes around a single point in the parameter space along different axes, any trends noticed could be applied more broadly to the simulation overall.
Parameters that maximize the chance of neither species going extinct are good, as it suggests the simulation is following the trajectories of the LVM.

To start, the group played around with the simulation manually in order to find a set of control/default parameters that allowed the simulation to frequently run for 500 steps without terminating early.
500 steps seemed like a reasonable threshold to check if a simulation run was stable.
The default parameters used are shown in the script below, along with some helper functions to grab the parameters needed to run different simulation functions.

#py_script("default_parameters", put_output: false, put_fname: true)

Each graph depicts a single parameter varied along a range of values.
For each value of the target parameter, 25 trials were run.
After which, the probabilities for each outcome were calculated.
The functions used to test the outcome chances and create a plot are shown below.
Note that each of these plots took about 30--60 minutes to _bake_.

#py_script("measure_outcome_chances", put_output: false, put_fname: true)

#let outcome_chance_test(attribute) = [
  #py_script("test_" + attribute, put_output: false)
  #figure(
    image("media/outcome_chances_" + attribute + ".svg", width: 80%),
    caption: [Outcome Chances vs #raw(attribute)],
  )
  #label("outcome_chances_" + attribute)
]

#pagebreak()

== `breed_time`

#outcome_chance_test("breed_time")

@outcome_chances_breed_time displays the outcome chances relative to the value of `breed_time` for the fish.
When the `breed_time` of the fish increases, the chances of the sharks going extinct also increases.
Since the fish take more steps before they can reproduce, their populations tend to grow more slowly, leaving the sharks with fewer sources of energy.
On the other hand, when the `breed_time` is too low, the fish clusters grow too quickly and start to merge together, making it more common for the sharks to consume all the fish on the board.
Thus, the LVM models the results better when the `breed_time` is not too high and not too low.

#pagebreak()

== `energy_gain`

#outcome_chance_test("energy_gain")

@outcome_chances_energy_gain displays the outcome chances relative to the value of `energy_gain` for the sharks.
When the sharks have a larger `energy_gain`, it allows their population to grow at a greater rate since they gain more energy from consuming fish.
Initial increases in `energy_gain` prevent the sharks from going extinct, as it helps them have more offspring exploring the board, discovering fish clusters, and keeping their species alive.
But if the `energy_gain` gets too high, the sharks start consuming too many fish clusters, making it more likely that sharks consume most or all of the fish clusters and subsequently die out.
Thus, the LVM models the results better when the `energy_gain` is not too low and not too high.
For the default parameters used, the best `energy_gain` range is about 5--13.

Note that the `energy_gain` had to be kept above a value of 1.
Since the sharks deplete 1 energy each time step, when `energy_gain = 1` it becomes impossible for the sharks to gain any energy overall and no new sharks can be born.
Since the shark population cannot grow under these conditions, these trajectories definitely do not follow the LVM.

#pagebreak()

== `breed_energy`

#outcome_chance_test("breed_energy")

@outcome_chances_breed_energy displays the outcome chances relative to the value of `breed_energy`.
Note that the `breed_energy` had to be kept higher than the the `start_energy`.
When `breed_energy` is less than or equal to `start_energy`, it can lead to cases where a shark dies or turns into a fish after giving birth.
This is due to the way creatures are stored in the `game_array`, using positive values for fish, negative values for sharks, and zero for unoccupied spaces.
Such behavior is definitely not desired.

As `breed_energy` increases, sharks need to eat more fish in order to have children.
As a result, sharks tend to hold onto more energy, swim around for longer, and have fewer offspring.
This makes sharks more dangerous and better able to hunt down fish clusters.
Thus, as `breed_energy` increases, the chances increase for sharks going extinct and for both species going extinct.
Whether these hardier sharks successfully take out all the fish clusters or leave a distant one remaining becomes almost a coin flip.
Therefore, the LVM models the results better when the `breed_energy` is not too high.
For the default parameters used, the best `breed_energy` range is about 10--14.

#pagebreak()

== `board_area`

#outcome_chance_test("board_area")

@outcome_chances_board_area displays the outcome chances as the `board_area` of the `game_array` is increased while the `aspect_ratio` is kept constant.
When the `board_area` is too small, the creatures are packed more tightly and fewer separate fish clusters form.
This makes it more common for the sharks to successfully eat all the fish cluster and leave none remaining, which makes both species go extinct.
When the `board_area` gets too large, the creatures on the board get more spread out.
This forces the sharks to travel further distances on average to find fish to eat, making it more likely that the sharks take out all fish or pass away before finding a new fish cluster.
Thus, too small or too large a `board_area` leads to higher chances of the extinction.
In other words, the LVM models the results better when the `board_area` is not too low and not too high.
For the default parameters used, this balanced `board_area` range is about 4400--6400.

#pagebreak()

== `aspect_ratio`

#outcome_chance_test("aspect_ratio")

@outcome_chances_aspect_ratio displays the outcome chances as the `aspect_ratio` of the `game_array` is changed while the `board_area` is kept constant.
A square board has an `aspect_ratio = 1` and is symmetric.
Increasing the `aspect_ratio` above 1 adds asymmetry to the board, making it take more steps to travel around one side compared to the other.
Higher `aspect_ratio` values lead to lower extinction chances.
The difference in distance to travel horizontally vs vertically around the board seems to desynchronize when shark fronts hunting along different axes collide, which helps prevent the fish population from getting too low.
Thus, the LVM models the result better when the `aspect_ratio` is higher.

#pagebreak()

== `initial_fish`

#outcome_chance_test("initial_fish")

@outcome_chances_initial_fish displays the outcome chances relative to the `initial_fish` value.
As the `initial_fish` value increases, more fish get scattered across the board with the potential to start clusters.
At first, increasing `initial_fish` reduces the chances of extinct.
With more food available, the sharks can more easily jump between fish clusters without the worry of being too far away from the next one or eating all of them.
But once `initial_fish` gets too high, the separate clusters start to merge together and the sharks consume larger clusters at a time, leaving the sharks more susceptible to leaving too few fish alive.
This reflects that starting with very low or high amounts of fish sets the populations on the outer streams predicted by the LVM.
Since these trajectories go fairly close to $x=0$ & $y=0$, it makes it more likely that the populations randomly reach zero and cause extinction.
Thus, the LVM models the results better when the `initial_fish` is not too low and not too high.
For the default parameters used, the best `initial_fish` range is about 700--900.

#pagebreak()

== `initial_sharks`

#outcome_chance_test("initial_sharks")

@outcome_chances_initial_sharks shows the outcome chances relative to the `initial_shark` value.
As the `initial_sharks` value increases, more sharks get scattered across the board.
At first increasing `initial_sharks` reduces the chance of sharks going extinct, but once `initial_sharks` gets too high the extinction chance starts to increase again.
This reflects that starting with very low or high amounts of sharsk sets the populations on the outer streams predicted by the LVM.
Since these trajectories go fairly close to $x=0$ & $y=0$, it makes it more likely that the populations randomly reach zero and cause extinction.
Thus, the LVM models the results better when the `initial_sharks` is not too low and not too high.
For the default parameters used, the best `initial_sharks` range is about 400--900.

#pagebreak()

== `start_energy`

#outcome_chance_test("start_energy")

@outcome_chances_start_energy displays the outcome chances relative to the `start_energy` of child sharks.
Note that the `start_energy` had to be kept lower than the the `breed_energy`.
When `start_energy` is greater than or equal to `breed_energy`, it can lead to cases where a shark dies or turns into a fish after giving birth.
This is due to the way creatures are stored in the `game_array`, using positive values for fish, negative values for sharks, and zero for unoccupied spaces.
Such behavior is definitely not desired.

Lower `start_energy` values correspond to lower extinction chances.
Since the `start_energy` for a newborn shark is taken from its parent, this suggests that it is better to leave most of the energy with the parent shark.
If a parent shark just had a child, it likely just ate a fish.
Due to the way sharks tend to form fronts that hunt down fish clusters, this puts the parent in a good position to eat another fish while the child gets put in a bad position with very few fish.
This helps the parent shark build up more energy, making it _stronger_ and better able to survive long enough to reach new fish clusters.
In contrast, the child gets put in a position where it is likely to die, even if it had more `start_energy`.
In other words, increasing `start_energy` hurts the parent more than it helps the child.
As a result, higher `start_energy` values lead to higher extinction chances.
Thus, the LVM models the results better when the `start_energy` is lower.

#pagebreak()

= Main Simulation Parameters

The three main simulation parameters are `breed_time`, `energy_gain`, and `breed_energy`.
These should relate in some way to the four LVM parameters $a$, $b$, $c$, and $d$.
While it is difficult to measure the LVM parameters directly, it is easier to measure the ratios $a/b$ and $d/c$.
When $x$ is at a local maximum, $y = d/c$.
When $y$ is at a local maximum, $x = a/b$.
In order to determine where those maxima are located, the population data was chunked into sections.
A section starts once population values go above some fraction of the population range, and it ends when the values go below a lower fraction of the range.
This method was chosen to deal with the random noise in the population data, avoiding falsely marking any small spikes as maxima.

Each graph depicts a single parameter varied along a range of values.
For each value of the target parameter, 25 trials were run.
The LVM ratios from each trial were averaged to get the values graphed.
In order to determine the ratios from a single trial's data, the critical points ($x_"crit" = a/b, y_"crit" = d/c$) were found using the method for locating local extrema described above, then the critical values were averaged to get the ratios.
Note that each of these plots took about 30--60 minutes to _bake_.

#py_script("measure_ratios", put_output: false, put_fname: true)

#let lvm_ratios_test(attribute) = [
  #py_script("test_" + attribute + "_ratios", put_output: false)
  #figure(
    image("media/lvm_ratios_" + attribute + ".svg", width: 90%),
    caption: [LVM Ratios vs #raw(attribute)],
  )
  #label("lvm_ratios_" + attribute)
]

#pagebreak()

== `breed_time`

#lvm_ratios_test("breed_time")

@lvm_ratios_breed_time plots the LVM ratios as `breed_time` is varied.
As `breed_time` increases, fish need to take more steps before they have children.
Since this a property of how rapidly the fish grow, it is not expected to only impact $d$ and not $a$, $b$, and $c$
This is reflected in the plot of $a/b$, as the ratio remains roughly constant as `breed_time` changes.
As `breed_time` gets larger, the fish reproduce more slowly $d$ is expected to decrease.
This is depicted in the graph of $d/c$, which shows the ratio decreasing as `breed_time` increases.

As shown in @outcome_chances_breed_time, both species very often go extinct when `energy_gain = 1`.
Since the simulation does not reflect the LVM under such conditions, it seems reasonable to ignore the sudden decrease in $a/b$ when `energy_gain = 1`.

#pagebreak()

== `energy_gain`

#lvm_ratios_test("energy_gain")

@lvm_ratios_energy_gain plots the LVM ratios as `energy_gain` is varied.
As noted when discussing @outcome_chances_energy_gain, the LVM models the situation best when `energy_gain` is kept within 5--13.
Thus, the trend in that portion of the graphs should be focused on.
Since `energy_gain` controls how much of an energy boost sharks get for eating fish, as it increases $b$ should increase too, helping the shark population grow more quickly.
$a$, $c$, and $d$ should not be impacted, since they have to do with different factors.
Thus, $d/c$ should remain constant and $a/b$ should decrease, both of which are depicted in the LVM ratio graphs.

#pagebreak()

== `breed_energy`

#lvm_ratios_test("breed_energy")

@lvm_ratios_breed_energy plots the LVM ratios as `breed_energy` is varied.
As `breed_energy` increases, sharks need to eat more fish in order to have children.
As a result, sharks can build up larger amounts of energy, allowing them to travel further distances.
As `breed_energy` increases, $b$ is expected to decrease since each fish eaten causes a smaller boost in the shark population.
In addition, higher `breed_energy` boosts shark longevity, thereby decreasing $a$.
The loss of 1 energy per move is less significant compared to the increased average shark energy.
If $a$ and $b$ decrease by similar amounts, that could cause their ratio to remain roughly the same, as depicted in the plot of $a/b$ in @lvm_ratios_breed_energy.

While `breed_energy` should have no impact on $d$, as that is a property of the fish exclusively, it could impact $c$.
As mentioned earlier, when `breed_energy` increases, sharks tend to hold onto more energy and swim around for longer.
This makes sharks more dangerous and better able to hunt down fish clusters, thereby increasing $c$
If $c$ increases while $d$ stays the same, that causes their ratio to decrease, as depicted in the plot of $d/c$ in @lvm_ratios_breed_energy.

#pagebreak()

= Circular Initialization

In the previous runs, the fish and sharks were initialized in the `game_array` at random locations.
In simulations that use circular initialization, the predators and prey are initially clustered in a circular group in the center of the `game_array`.
The sharks form a central disk, with the fish creating a ring around them.

This setup leads to different dynamics.
Due to the fact that the sharks and fish start close to each other, the sharks encounter the fish immediately and a chase outward to the edges of the board ensues.
As the diameter widens and the sharks get spread more thinly, some fish sneak into the center.
What follows is a more consistent interaction between the species.
With random initialization, most of the fish clusters grow and shrink in phase with each other.
In contrast, when using circular initialization the fish clusters tend to grow and shrink out of phase with each other, making it easier for both species to maintain steady levels and avoid going extinct.
This is reflected in the pattern that the chance of neither species going extinct went up for most points in all graphs when compared to their random initialization values.

#let outcome_chance_test_circular(attribute) = [
  #py_script("test_" + attribute, put_output: false)
  #figure(
    image("media/outcome_chances_" + attribute + "_circular.svg", width: 80%),
    caption: [Outcome Chances vs #raw(attribute) (Circular Initialization)],
  )
  #label("outcome_chances_" + attribute + "_circular")
]

#let lvm_ratios_test_circular(attribute) = [
  #py_script("test_" + attribute + "_ratios_circular", put_output: false)
  #figure(
    image("media/lvm_ratios_" + attribute + "_circular.svg", width: 90%),
    caption: [LVM Ratios vs #raw(attribute) (Circular Initialization)],
  )
  #label("lvm_ratios_" + attribute + "_circular")
]

== `breed_time`

#outcome_chance_test_circular("breed_time")

@outcome_chances_breed_time_circular displays the outcome chances relative to the value of `breed_time` for the fish when circular initialization is used.
When compared to @outcome_chances_breed_time with random initialization, the overall shapes are similar.
When the `breed_time` increases, the chances of the sharks going extinct also increases.
But with circular initialization, the chance of neither species going extinct is noticeably higher and decreases more slowly.

#lvm_ratios_test_circular("breed_time")

@lvm_ratios_breed_time_circular plots the LVM ratios as `breed_time` is varied when circular initialization is used.
When compared to @lvm_ratios_breed_time with random initialization, the graph of $d/c$ decreases in both.
If the graph of $a/b$ for circular initialization is focused on in the region where the neither extinct chance is high, 2--7, then it remains roughly constant as in the graph for random initialization.

#pagebreak()

== `energy_gain`

#outcome_chance_test_circular("energy_gain")

@outcome_chances_energy_gain_circular displays the outcome chances relative to the value of `energy_gain` for the sharks when circular initialization is used.
When compared to @outcome_chances_energy_gain with random initialization, the overall shapes are similar.
When `energy_gain` gets too large, the extinction chances start to increase.
But with circular initialization, smaller `energy_gain` values can be supported without causing extinction.
The circular initialization helps keep the sharks closer to the fish, which allows the simulation to keep going even when sharks do not get as much of an energy boost from eating fish.

#pagebreak()

#lvm_ratios_test_circular("energy_gain")

@lvm_ratios_energy_gain_circular plots the LVM ratios as `energy_gain` is varied when circular initialization is used.
When compared to @lvm_ratios_energy_gain with random initialization, the overall shapes are very similar.
Thus, circular initialization does not noticeably change how `energy_gain` impacts the LVM ratios.

#pagebreak()

== `breed_energy`

#outcome_chance_test_circular("breed_energy")

@outcome_chances_breed_energy_circular displays the outcome chances relative to the value of `breed_energy` with circular initialization.
The chance of both species surviving remains close to 1 regardless of `breed_energy`.
In contrast, in @outcome_chances_breed_energy with random initialization the extinction chances start to rise when `breed_energy` gets too high.
Even though the sharks get hardier and hold on to more energy when `breed_time` is large, they still do not consume too many fish.
The circular initialization helps remove powerful sharks with lots of energy more regularly, preventing them eating more fish clusters than they should.

#lvm_ratios_test_circular("breed_energy")

@lvm_ratios_breed_energy_circular plots the LVM ratios as `breed_energy` is varied with circular initialization.
As `breed_time` increases, $a/b$ increases while $d/c$ remains roughly constant.
In contrast, @lvm_ratios_breed_energy with random initialization showed $a/b$ remaining constant and $d/c$ decreasing.
Since the circular initialization makes sharks with lots of energy less of a threat, that could have caused changes in `breed_energy` to no longer impact $a$ or $c$, factors that previously relied on changes in shark longevity.
But $b$ should still decrease as `breed_energy` increases, since sharks that need more energy to breed produce fewer offspring after eating fish.
That would result in $a/b$ increasing and $d/c$ remaining constant as `breed_energy` gets larger, which is the pattern observed in @lvm_ratios_breed_energy_circular.

#pagebreak()

== `board_area`

#outcome_chance_test_circular("board_area")

@outcome_chances_board_area_circular displays the outcome chances relative to the `board_area` with circular initialization.
When compared with @outcome_chances_board_area, the graphs have similar shapes when the `board_area` is low.
But as the `board_area` gets larger, simulations using circular initialization are better able to support the populations with lower chances of them going extinct.
Perhaps the initial chase at the start of circular initialization helps spread the creatures more evenly and out of sync.
That prevents either population from getting too low in the oscillations that follow.
This effect could happen regardless of `board_area`, assuming it is sufficiently large.

#pagebreak()

== `aspect_ratio`

#outcome_chance_test_circular("aspect_ratio")

@outcome_chances_aspect_ratio_circular displays the outcome chances relative to the `aspect_ratio` with circular initialization.
The extinction chances remain very close to 0 for all `aspect_ratio` values.
In contrast, @outcome_chances_aspect_ratio shows that simulations with higher `aspect_ratio` values do better when random initialization is used.
This suggests that the out of phase fish clusters that characterize circular initialization get created regardless of `aspect_ratio`.
Whether the expanding fish+shark ring reaches the top+bottom edges of the board at the same time as the left+right edges does not effect the outcome chances.
Perhaps fish sneaking inside the expanding ring is what leads to the desynced clusters that help simulations with circular initialization avoid extinction, as that can occur in similar ways no matter what the `aspect_ratio` is.

#pagebreak()

== `initial_fish`

#outcome_chance_test_circular("initial_fish")

@outcome_chances_initial_fish_circular displays the outcome chances relative to the `initial_fish` with circular initialization.
When compared with @outcome_chances_initial_fish with random initialization, the overall graph shapes are similar.
Initially, increases in `initial_fish` cause extinction chances to drop.
Then, outcome chances remain constant for a period.
Finally, the extinction chances start to rise again as `initial_fish` gets larger.
In contrast, the simulations with circular initialization seem to have higher chances of neither species going extinct for a wider range of `initial_fish` values.
This suggests that circular initialization is more flexible in regards to the starting number of fish, since many of them get eaten as soon as the expanding ring of fish+sharks reaches the edges of the `game_array`.

#pagebreak()

== `initial_sharks`

#outcome_chance_test_circular("initial_sharks")

@outcome_chances_initial_sharks_circular shows the outcome chances relative to the `initial_shark` with circular initialization.
Unlike with random initialization where setting `initial_sharks` too high or too low causes extinction chances to rise, a trend depicted in @outcome_chances_initial_sharks, circular initialization seems to have low extinction chances regardless of the `initial_sharks` value.
Many of the sharks that start in the center of the disk die early.
They do not get an opportunity to eat any fish because the sharks on the outer edge of the disk block them.
As a result, simulations that use circular initialization are not noticeably impacted by the `initial_sharks` value.

#pagebreak()

== `start_energy`

#outcome_chance_test_circular("start_energy")

@outcome_chances_start_energy_circular displays the outcome chances relative to the `start_energy` with circular initialization.
The chances of neither species going extinct are higher compared to @outcome_chances_start_energy with random initialization.
In addition, with circular initialization there is no noticeable increase in extinction chances as `start_energy` rises.
Having parent sharks build up more energy no longer makes them more dangerous hunters, as the circular initialization helps keep the population churning and makes sure enough child sharks are not too far away from their next fish cluster.

#pagebreak()

= Modified Lotka-Volterra Model

The differential equations of the LVM do not set any hard limit on the sizes of the predator or prey populations.
In the absence of predators ($y=0$), $(d x)/(d t) = +d x$, suggesting that the prey will experience exponential growth indefinitely.
For the predators, so long as $a y < b x y$, the predator population will continue to grow.
In contrast, population sizes in the Wa-Tor simulation are limited by the dimensions of the `game_array`.
Each nonempty cell can only hold one shark or fish, so both population sizes are capped at the total number of cells in the `game_array`.
Thus, it seems reasonable to modify the LVM to have terms that involve a carrying capacity ($N_oo$) for both predators and prey.

To start, the $+d x$ term could be changed into $+d x (1 - x/N_oo)$ to model the effects of scarcity and competition between prey.
The $+d(1 - x/N_oo)$ portion acts like a variable growth rate of the prey.
This variable grow rate starts close to $d$ when $x$ is small, then decreases as $x$ gets larger.
When $x=N_oo$, that variable growth rate equals 0, reflecting the limitation that no growth can occur beyond the carrying capacity.
In the simulation, fish need to move into empty cells in order to accumulate time and eventually produce an offspring once they reach the `breed_time` requirement.
Since the supply of empty cells is limited, fish effectively compete for those free spaces.
As more cells get occupied, less fish are able to move and reproduce, thereby limiting the growth rate.
And if fish filled the board, no further growth could occur since there are no more spaces to move into.

Next, the $+b x y$ term could be changed into $+b x y (1 - y/N_oo)$ to model the effects of competition between predators.
The $+b (1 - y/N_oo)$ portion acts like a variable proportionality of the predator's growth rate.
This proportionality starts close to $b$ when $y$ is small, then decreases as $y$ gets larger.
When $y=N_oo$, that proportionality equals 0, reflecting the limitation that no growth can occur beyond the carrying capacity.
In the simulation, sharks produce offspring once their energy passes the `breed_energy` requirement and they have an open space to move into.
Sharks gain energy from eating fish and lose 1 energy each step of the simulation.
In short, sharks need to eat fish and be next to an empty cell in order to reproduce.
When the number of sharks is low, they can easily reach the fish and achieve lots of growth.
But as more cells get occupied by sharks, they block each other from reaching the fish more frequently.
Once overcrowding starts to take effect, additional sharks do not help boost the population growth any further since those extra hunters are stuck idling.
And if sharks filled the board, no further growth could occur since there are no more spaces to move into.

Finally, the $-c y x$ term could be changed into $-c y x (1 - y/N_oo)$ for similar reasons as the modification to $+b x y$.
As more sharks fill the board, not as many additional fish get eaten due to the sharks starting to crowd each other out.

Making those changes yields the following modified Lotka-Volterra Model.
$
(d y)/(d t) = -a y + b x y (1 - y/N_oo) quad (d x) / (d t) = +d x (1 - x/N_oo) - c y x (1 - y/N_oo)
$

Running the simulation using the `simulation_playground.py` script with the default parameters set yields the plot shown in @sample_plot_default_parameters.
Notice that the paths on the stream plot tend to spiral counterclockwise inward.
In contrast, the streams of the LVM form closed loops and stay at fixed levels, as shown in @lvm_stream_plot.
But with the modified LVM depicted in @lvm_modified_stream_plot, the streams spiral inward similar to what was seen in @sample_plot_default_parameters.
Thus, this adjusted model successfully captures additional aspects of the simulation behavior.

#figure(
  image("media/sample-plot-default-parameters.svg", width: 80%),
  caption: [Sample Plot with Default Parameters],
) <sample_plot_default_parameters>

#py_script("lvm_stream_plot", put_output: false)
#figure(
  image("media/lvm_stream_plot.svg", width: 80%),
  caption: [LVM Stream Plot],
) <lvm_stream_plot>

#py_script("lvm_modified_stream_plot", put_output: false)
#figure(
  image("media/lvm_modified_stream_plot.svg", width: 80%),
  caption: [Modified LVM Stream Plot],
) <lvm_modified_stream_plot>

#pagebreak()

= Simulation Code

#py_script("wa_tor", put_output: false, put_fname: true)

#py_script("simulation_playground", put_output: false, put_fname: true)

#py_script("stream_plotter", put_output: false, put_fname: true)
