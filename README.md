# Swarm Robotics Simulation Project

## Project Abstract

The interest in, application of and possibilities offered by swarm robotics and active matter promote the need for research and development into our understanding of collective intelligence. Swarm dynamics are observed throughout nature due to their ability to produce complex yet robust and efficient macroscopic behaviours from microscopic simplicity. Active matter outlines the equations of motion of collectives offering unique insight into the underlying mechanics displayed by living and non-living systems. The combination of these features offer many advantages for similar robotic systems and illustrate how they may be utilised for our benefit. This report describes the investigation into the collaboration of run-and-tumble motion with the anti-Vicsek/alignment model as a collective behaviour for a swarm of Kilobots. Simulations demonstrate the effective dynamics and parameters of the model when compared to traditional alignment and random movement. Experiments examine how this behaviour can be implemented onto a real-world system using simple robotic agents. The importance of combining simulation with experimentation is outlined as a key factor in the development of collective dynamics, exemplifying how both can be utilised in the effective deployment of swarms to the desired application.

### Prerequisites
- Python 3.11 or later
- Required Python libraries: `scipy`, `pygame`
- Optional Python libraries for data analysis: `matplotlib`, `seaborn`, `pandas`, `cv2`, `numpy` 
- Optional Python libraries for pattern generation: `PIL`
- Kilobots, Kilogui, Overhead Controller (for real-world experiments)
- Kilolib library, c to Hex build file (for C code)

### Installation
1. Clone the repository:
https://github.com/ks20447/Technical_Project.git

2. Install Python dependencies to virtual environment

## Usage

### Simulation
To run the simulation, execute:
python pygamesim.py

This will start a simulation based on parameters set in `config.json`.

### Experimentation
To upload the C code to Kilobots for real-world testing:
1. Connect your overhead controller to the computer
2. Convert `kilobot_code.c` to Hex file
3. Set Kilobots to Bootload via Kilogui application
4. Upload to Kilobots
5. Run


## Configuration
- **Simulation Parameters:** Modify `Data/config.json` to adjust parameters.
- **Kilobot Behavior:** Edit global parameters to change the robot's algorithms.

## Acknowledgments
- This project was constructed under the supervision of Dr Stuart Thompson and Prof Sabine Hauert of the University of Bristol

## Contact
For any queries or discussions, please open an issue on GitHub or contact adam@junction42.com.

