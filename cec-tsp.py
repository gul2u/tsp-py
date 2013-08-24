#!/usr/bin/python

'''
CodeEval Submission for Commuting Engineer Challenge
Submitted by Thomas Chen
'''

import sys
import time
import random
import argparse
from math import sqrt
import urllib2

import json
from pprint import pprint

#import re


def hillclimb(init_function,move_operator,objective_function,max_evaluations):
    '''
    hillclimb until either max_evaluations is reached or we are at a local optima
    '''
    best=init_function()
    best_score=objective_function(best)
    
    num_evaluations=1
    
    while num_evaluations < max_evaluations:
        # examine moves around our current position
        move_made=False
        for next in move_operator(best):
            if num_evaluations >= max_evaluations:
                break
            
            # see if this move is better than the current
            next_score=objective_function(next)
            num_evaluations+=1
            if next_score > best_score:
                best=next
                best_score=next_score
                move_made=True
                break # depth first search
            
        if not move_made:
            break # we couldn't find a better move (must be at a local maximum)
    
    return (num_evaluations,best_score,best)

def hillclimb_and_restart(init_function,move_operator,objective_function,max_evaluations):
    '''
    repeatedly hillclimb until max_evaluations is reached
    '''
    best=None
    best_score=0
    
    num_evaluations=0

    while num_evaluations < max_evaluations:
        remaining_evaluations=max_evaluations-num_evaluations
        
        evaluated,score,found=hillclimb(init_function,move_operator,objective_function,remaining_evaluations)
        
        num_evaluations+=evaluated
        if score > best_score or best is None:
            best_score=score
            best=found
        
    return (num_evaluations,best_score,best)

def reversed_sections(tour):
    '''generator to return all possible variations where the section between two cities are swapped'''
    for i,j in all_pairs(len(tour)):
        if i != j:
            copy=tour[:]
            if i < j:
                copy[i:j+1]=reversed(tour[i:j+1])
            else:
                copy[i+1:]=reversed(tour[:j])
                copy[:j]=reversed(tour[i+1:])
            if copy != tour: # no point returning the same tour
				if copy[0] == 0:			  # tour must start from location 0
					yield copy
				elif copy[-1] == 0:
					yield copy[::-1]				  

def swapped_locations(tour):
    '''generator to create all possible variations where two cities have been swapped'''
    for i,j in all_pairs(len(tour)):
        if i < j and i != 0:
            copy=tour[:]
            copy[i],copy[j]=tour[j],tour[i]
            yield copy

def all_pairs(size,shuffle=random.shuffle):
    '''generates all i,j pairs for i,j from 0-size uses shuffle to randomise (if provided)'''
    r1=range(0,size)
    r2=range(0,size)
    if shuffle:
        shuffle(r1)
        shuffle(r2)
    for i in r1:
        for j in r2:
            if j != 0:
            	yield (i,j)

def distance_matrix(coords):
	'''create a distance matrix using Google Maps API based on location coordinates'''
	matrix={}
	url = "http://maps.googleapis.com/maps/api/distancematrix/json?"
	origins = "origins="
	destinations = "&destinations="
	locations = ""

	for loc in coords:
		locations+=str(loc[0])+','+str(loc[1])
		if loc != coords[-1]:
			locations += '|'

	origins+=locations
	destinations+=locations

	dm_data = json.load(urllib2.urlopen(url+origins+destinations+"&sensor=false"))
	#pprint(dm_data)

	#dm_response=open("gmaps-response.json")
	#dm_data=json.load(dm_response)

	for i,r in enumerate(dm_data["rows"]):
		for j,path in enumerate(r["elements"]):
			matrix[i,j] = path["distance"]["value"]
			#matrix[i,j] = path["duration"]["value"]

	return matrix

def cartesian_matrix(coords):
    '''create a distance matrix for the city coords that uses straight line distance'''
    matrix={}
    for i,(x1,y1) in enumerate(coords):
        for j,(x2,y2) in enumerate(coords):
            dx,dy=x1-x2,y1-y2
            dist=sqrt(dx*dx + dy*dy)
            matrix[i,j]=dist
    return matrix

def tour_length(matrix,tour):
    '''total up the total length of the tour based on the distance matrix'''
    total=0
    num_locations=len(tour)
    for i in range(num_locations):
        j=(i+1)%num_locations
        loc_i=tour[i]
        loc_j=tour[j]
        if j != 0:			# travel route is acyclic
        	total+=matrix[loc_i,loc_j]
    return total

def init_random_tour(tour_length):
   #tour=range(tour_length)
   tour=range(1,tour_length)
   random.shuffle(tour)
   return [0]+tour

def read_coords(coord_file):
    '''
    read the coordinates from file and return the distance matrix.
    coords should be stored as comma separated floats, one x,y pair per line.
    '''
    coords=[]

    for line in coord_file:
        coord_index=line.find("(")
        x,y=line.strip()[coord_index:].split(",")
        x=x.replace("(","")
        y=y.replace(")","")
        coords.append((float(x),float(y)))
    return coords

def main():
	parser=argparse.ArgumentParser()
	parser.add_argument('file',nargs=1)
	args=parser.parse_args()
    
	#move_operator = swapped_locations
	move_operator = reversed_sections
	max_iterations = 40000

	# Input file and store coordinates
	coord_file = args.file[0]
	coords = read_coords(file(coord_file))
	#coords = [(37.7768016, -122.4169151),(37.7860105, -122.4025377),(37.7821494, -122.4058960),(37.7689269, -122.4029053),(37.7768800, -122.3911496),(37.7706628, -122.4040139),(37.7870361, -122.4039444),(37.7507903, -122.3877184),(37.7914417, -122.3927229),(37.8672841, -122.5010216)]
	#coords = [(37.7768016, -122.4169151),(37.7860105, -122.4025377),(37.7821494, -122.4058960),(37.7689269, -122.4029053),(37.7768800, -122.3911496),(37.7706628, -122.4040139)]

	# Initialize random tour
	init_function=lambda: init_random_tour(len(coords))
	#tour = init_random_tour(len(coords))

	# Construct distance matrix
	matrix=cartesian_matrix(coords)
	#matrix=distance_matrix(coords)
	#pprint(matrix)

	# Define objective_function
	objective_function=lambda tour: -tour_length(matrix, tour)


	# Execute hill_climb
	iterations,score,best=hillclimb_and_restart(init_function,move_operator,objective_function,max_iterations)

	for loc in best:
		print loc+1
	
	#print tour_length(matrix,best)

if __name__ == "__main__":
	#beginTime=int(round(time.time()*1000))

	main()

	#endTime=int(round(time.time()*1000))
	#print "Run time:", endTime-beginTime