# NaturalLanguageGenerator
*A Natural Language Generator based on the Markov Chain*
This project was written for the Hillview Middle School STEM Fair and/or the San Mateo County STEM Fair, licensed under the GNU General Public License v3.0. Please open LICENSE for more legal information. This is not a legal document.

## The Natural Language Generator
The Natural Language Generator is an extendable NLP Class based on the Markov Memoryless Principle -- where the future state is only based on the current state of an object, hence memoryless -- developed by Andrey Markov. The Natural Language Generator ("The Generator") is made based on the same principle, inferring words based on the current state of the text.

## The Project
Based on this generator, the developer will train the module with two different corpuses -- one collected from the public and one prewritten -- and separately evaluate the performance, the grammatical accuracy and the comprehensiveness of the generated data. The results will be open-sourced in this repository.

## Extensibility
The system is well documented and easy to extend to. All data information can be stored and retrieved with a single object. The class is able to be pickled and stored into a binary file for later access. Please feel free to fork, edit, and open pull requests as needed.

## System Requirements and Dependencies
1. Python ~ 3.6.1 (v3.6.1:69c0db5050) and core libraries
2. SciPy ~ 0.19.1
3. NumPy ~ 1.13.3
