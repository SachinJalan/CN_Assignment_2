## Computer Networks Assignment 2

This repository contains the assingment given as a part of the course CS:433 Computer Networks at IIT Gandhinagar.  
The assignment can be found in the repository.

### Requirenments

To run the assignment you need to have mininet properly installed along with the openvswitch. The system will also require wireshark to observe the packets properly, python 2.7+ is required.

### Steps to run

#### Question 1
Step 1: First clone this repository into your local system.
```
git clone https://github.com/SachinJalan/CN_Assignment_2
```
Step 2:
```
sudo python3 question1.py
```
Ensure that you have root privledges, and run the code in root mode. After these steps you will see the mininet CLI open and pingall command would have been executed to check the connectivity of all the hosts. The executed topology can be found in the report present in the repository.

#### Question 2 
To execute question 2 follow the given steps:  
Step 1:  
```
sudo python3 question2.py --config=b --congestion=reno --loss=0
```

The options have the following meaning:  
- Config : It is used to choose the type of simulation, single client or multi client. Passing option as b will result in single client connection while passing argument c will result in simulation of 3 clients
- Congestion : It selects the type of congestion control scheme to be used it is a compulsary argument to be given. Some options are vegas, reno, bbr, cubic
- Loss : It sets the percentage loss of packets between the link s1 and s2, the two switches which connect the network. argument to be passed in loss option is any number between 0-100 both inclusive.  

#### Team Members
Sachin Jalan - 21110183  
Anushk Bhana - 21110031