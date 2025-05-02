# ENGR 285 --- Project 1

This repository contains my group's work for Project 1 of my Engineering 285 class.
The assignment focuses on modeling predator-prey dynamics using the Lotka-Volterra Model.
The population data is generated using a [Wa-Tor](https://en.wikipedia.org/wiki/Wa-Tor) simulation.

The document is created using [Typst](https://typst.app/).
A `makefile` is configured to run all the Python scripts in the `scripts` directory and save their text output in the `output` directory.
The scripts and output can then be included in the document as desired.
The `makefile` also compiles the Typst document into a PDF.

## Comments from Professor

> First Objective:
> Very concise and to-the-point, well-discussed.
> 
> Second Objective:
> Very systematic approach to the variation of parameters;
> thoroughly answered the question of when the populations will survive.
> I was hoping for a little more than just all types of oscillation, since LVM oscillation is perfectly periodic, but I’m still happy with the level of analysis you did.
> 
> Third Objective:
> Love the approach, probably the best I’ve seen.
> 10/10 no notes.
> 
> Fourth Objective:
> Again, very concise and to-the-point, well-discussed.
> 
> Extending Objective:
> Good attempt at a new model!
> It’s probably a little better to assign the carrying capacity to the total of x+y (so you’d have factors of (1-(x+y)/N_inf) instead), and I don’t think the fish death rate needs limiting (since things are allowed to die as fast as they want).
> While your model does have the spiraling you see in the data (love those graphs!!), it doesn’t look like it has the same profile/shape.
> 
> Overall:
> Pleasure to read, excellent job!
> 
> Grade: 90/90
