Chromophage
===========

**Simulated organisms that eat and poop colors in Python3**

Introduction
---------

Chromophage simulates the colonization of an image file by a self-replicating organism which eats values from the integer representation one of the 8-bit RBG color channels of a pixel, while excreting values of another color.

The turn-based simulation treats an image as a petri dish which is inoculated with a simple organism, the chromophage. The phage will consume its food color, excrete its waste color, and reproduce through a duplicative process. Phages can starve to death, die of old age, and phages will move from pixel to pixel in search of food.

Examples
---------

![Original Image](http://i.imgur.com/BkQUI3U.gif "")  
A single initial phage completely colonizes an image over 300 turns.  
50 turns / frame.

![Original Image](http://i.imgur.com/rjhCHQ1.gif "")  
Three initial phages colonize an image to extinction over 550 turns.  
50 turns / frame.


	
Phage Behavior 
--------- 
**Eating and Excreting**   
At any given time, a phage is living on a specific pixel. Each turn, a phage will attempt to consume 2<sup>n</sup> from the integer value of the 8-bit digital color channel it identifies as food. If the integer value of the color channel is smaller than 2<sup>n</sup>, the phage is unable to eat. If the phage was able to eat the previous turn, it will excrete 2<sup>m</sup> of its waste color, adding the value to the appropriate color channel.  

Taking the red, blue, and green color channels as 0, 1, and 2 respectively, the integer value of attributes `phage.food` and `phage.waste` and used to identify the appropriate RBG color channel to modify. The integer values of *n* and *m* are set by attributes `phage.consume` and `phage.excrete`.
 
**Movement**   
Phages will move to the neighboring pixel with the highest ratio of food to waste, adjusted for the number of phages living on that pixel. 
 
**Health**   
Phages have a maximum health established at the start of the simulation, `phage.health_max`. Phages with any health, `phage.health > 0`, will attempt to eat, poop, and move. A separate minimum health value limits reproduction. 
 
Each turn, a phage which ate the previous turn, `phage.full == True`, will generate one health, `phage.health += 1`. One health will be lost if excessive waste is present. Over-population will result in population proportionate health penalties. These functions are affected by the `phage.waste_immunity` and `phage.pop_immunity` attributes.

The `phage.old_age` attribute is used to control phage life span. When a phage is "old", `phage.age >= phage.old_age`, it begins to take a health penalty each turn, `phage.health -= (phage.age - phage.old_age)`.
 
**Reproduction**   
Reproduction is governed by a counter attribute, `phage.reproduction_cooldown_counter`, and a minimum health attribute, `phage.minimum_reproductive_health`. When the countdown is complete, if a phage's health is equal to or greater than the minimum health, it will add a copy of itself to the simulation phage colony. The age attribute of this copy is set to zero, `phage.age = 0`, and the health of the copy is reset to maximum, `phage.health = phage.health_max`.
 


