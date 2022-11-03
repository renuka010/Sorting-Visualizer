import pygame
import random
import math

pygame.init()

class DrawInformation:
	BLACK=0,0,0
	WHITE=255,255,255
	RED=195, 26, 253 

	GREEN=250, 26, 253  
	BLUE=0,0,255
	FINAL=[(157,248,85),(90,248,85)]
	BACKGROUND_COLOR=WHITE
	GRADIENTS = [(128,128,128),(160,160,160),(192,192,192)]

	FONT = pygame.font.SysFont('Segoe UI', 25)
	LARGE_FONT = pygame.font.SysFont('Segoe UI', 35)

	SIDE_PAD=100
	TOP_PAD=150

	color_final=set()

	def __init__(self, width, height, mylist):
		self.width=width
		self.height=height

		self.window=pygame.display.set_mode((width,height))
		pygame.display.set_caption("Sorting Algorithm Visualizer")
		self.set_list(mylist)

	def set_list(self, mylist):
		self.mylist=mylist
		self.min_val=min(mylist)
		self.max_val=max(mylist)

		self.block_width= math.floor((self.width - self.SIDE_PAD) / len(mylist))
		self.block_height= math.floor((self.height-self.TOP_PAD) / (self.max_val-self.min_val))
		self.start_x= self.SIDE_PAD//2

def draw(draw_info, algo_name, ascending):
	draw_info.window.fill(draw_info.BACKGROUND_COLOR)
	
	title = draw_info.LARGE_FONT.render(f"{algo_name}-{'Ascending' if ascending else 'Descending'}", 1, (237, 44, 6 ))
	draw_info.window.blit(title,(draw_info.width/2 - title.get_width()/2,5))

	controls = draw_info.FONT.render("R - Reset | SPACE - Start sorting | A - Ascending| D - Decending", 1, draw_info.BLACK)
	draw_info.window.blit(controls,(draw_info.width/2 - controls.get_width()/2,45))

	sorting = draw_info.FONT.render("B - Bubble Sort | I - Insertion Sort | M - Merge Sort | Q - Quick Sort | H - Heap Sort", 1, draw_info.BLACK)
	draw_info.window.blit(sorting,(draw_info.width/2 - sorting.get_width()/2,75))

	draw_list(draw_info)
	pygame.display.update()

def draw_list(draw_info, color_positions={}, clear_bg=False):
	mylist=draw_info.mylist

	if clear_bg:
		clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width-draw_info.SIDE_PAD, draw_info.height-draw_info.TOP_PAD)
		pygame.draw.rect(draw_info.window,draw_info.BACKGROUND_COLOR, clear_rect)

	for i, val in enumerate(mylist):
		x=draw_info.start_x + i * draw_info.block_width
		y=draw_info.height - (val - draw_info.min_val+1)*draw_info.block_height
		color = draw_info.GRADIENTS[i%3]
		
		if i in draw_info.color_final:
			color=draw_info.FINAL[i%2]

		if i in color_positions:
			color=color_positions[i]

		pygame.draw.rect(draw_info.window,color,(x,y,draw_info.block_width,draw_info.height))

	if clear_bg:
		pygame.display.update()

def generate_list(n, min_val, max_val):
	mylist=[]

	for _ in range(n):
		val=random.randint(min_val, max_val)
		mylist.append(val)

	return mylist

def bubble_sort(draw_info, ascending=True):
	mylist = draw_info.mylist

	for i in range(len(mylist)-1):
		for j in range(len(mylist)-1):
			num1=mylist[j]
			num2=mylist[j+1]
			if (num1>num2 and ascending) or (num1<num2 and not ascending):
				mylist[j], mylist[j+1] = mylist[j+1], mylist[j]
				draw_list(draw_info,{j: draw_info.GREEN, j+1: draw_info.RED},True)
				yield True
		draw_info.color_final.add(j-i+1)
	draw_info.color_final.add(0)

	return mylist
	
def insertion_sort(draw_info, ascending=True):
	mylist = draw_info.mylist

	for i in range(1,len(mylist)):
		current=mylist[i]

		while True:
			ascending_sort = i>0 and mylist[i-1]>current and ascending
			descending_sort = i>0 and mylist[i-1]<current and not ascending

			if not ascending_sort and not descending_sort:
				break
			mylist[i]=mylist[i-1]
			i=i-1
			mylist[i]=current
			draw_list(draw_info, {i-1: draw_info.GREEN, i: draw_info.RED}, True)
			yield True
	for i in range(len(mylist)):
		draw_info.color_final.add(i)

	return mylist

def refill(draw_info,i,j):
	draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED}, True)
	pygame.display.update()

def merge_sort(draw_info,array, l, r, ascending=True):
	mid =(l + r)//2
	if l<r:
		yield from merge_sort(draw_info,array, l, mid, ascending)
		yield from merge_sort(draw_info,array, mid + 1, r, ascending)

		i = l
		j = mid+1
		x1=l
		y1=mid
		x2= mid+1
		y2=r
		temp =[]
		while i<= y1 and j<= y2:
			refill(draw_info,i,j)
			yield True
			if array[i]<array[j] and ascending:
				temp.append(array[i])
				i+= 1
			elif array[i]>array[j] and not ascending:
				temp.append(array[i])
				i+= 1
			else:
				temp.append(array[j])
				j+= 1
		while i<= y1:
			refill(draw_info,i-1,i)
			yield True
			temp.append(array[i])
			i+= 1
		while j<= y2:
			refill(draw_info,j-1,j)
			yield True
			temp.append(array[j])
			j+= 1
		j = 0    
		for i in range(x1, y2 + 1):
			if(x1==0 and y2+1==len(array)):
				draw_info.color_final.add(i)
			refill(draw_info,i,i+1)
			yield True
			array[i]= temp[j]
			j+= 1

def quick_sort(draw_info,array, low, high, ascending=True):
	if low <= high:

		pivot = array[high]

		i = low - 1

		for j in range(low, high):
			draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED, high: draw_info.BLUE}, True)
			yield True
			if (array[j] <= pivot and ascending) or (array[j] >pivot and not ascending):
				i = i + 1
				(array[i], array[j]) = (array[j], array[i])
			draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED, high: draw_info.BLUE}, True)
			yield True
	
		(array[i + 1], array[high]) = (array[high], array[i + 1])
		draw_list(draw_info, {i+1: draw_info.GREEN, high: draw_info.RED}, True)
		yield True

		pi = i+1
		draw_info.color_final.add(pi)

		yield from quick_sort(draw_info,array, low, pi-1, ascending)

		yield from quick_sort(draw_info,array, pi+1, high, ascending)
	
def heapify(draw_info, arr, n, i, ascending):
	largest = i
	l = 2 * i + 1
	r = 2 * i + 2

	draw_list(draw_info, {i: draw_info.GREEN, largest: draw_info.RED}, True)
	yield True
	if (l < n and arr[i] < arr[l] and ascending) or (l<n and arr[i] > arr[l] and not ascending):
		largest = l

	draw_list(draw_info, {largest: draw_info.GREEN, r: draw_info.RED}, True)
	yield True
	if (r < n and arr[largest] < arr[r] and ascending) or (r < n and arr[largest] > arr[r] and not ascending):
		largest = r

	draw_list(draw_info, {i: draw_info.GREEN, largest: draw_info.RED}, True)
	yield True 
	if largest != i:
		(arr[i], arr[largest]) = (arr[largest], arr[i])

		yield from heapify(draw_info, arr, n, largest, ascending)

def heap_sort(draw_info, ascending=True):
	n = len(draw_info.mylist)
	arr=draw_info.mylist

	for i in range(n // 2 - 1, -1, -1):
		yield from heapify(draw_info, arr, n, i, ascending)

	for i in range(n - 1, 0, -1):
		(arr[i], arr[0]) = (arr[0], arr[i])
		draw_info.color_final.add(i)
		yield from heapify(draw_info, arr, i, 0, ascending)
	draw_info.color_final.add(0)

def main():
	run=True
	clock=pygame.time.Clock()

	n=70
	min_val=1
	max_val=100

	mylist=generate_list(n,min_val,max_val)
	draw_info=DrawInformation(1000,550,mylist)

	sorting=False
	ascending=True

	sorting_algorithm=bubble_sort
	sorting_algo_name="Bubble Sort"
	sorting_algorithm_generator=None

	while run:
		clock.tick(20)

		if sorting:
			try:
				next(sorting_algorithm_generator)
			except StopIteration:
				sorting = False
		else:
			draw(draw_info, sorting_algo_name, ascending)

		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				run=False

			if event.type != pygame.KEYDOWN:
				continue

			if event.key == pygame.K_r:
				mylist=generate_list(n,min_val,max_val)
				draw_info.set_list(mylist)
				draw_info.color_final=set()
				sorting=False
			elif event.key == pygame.K_SPACE and sorting==False:
				sorting=True
				if sorting_algo_name=="Merge Sort" or sorting_algo_name=="Quick Sort":
					sorting_algorithm_generator=sorting_algorithm(draw_info, draw_info.mylist, 0, len(draw_info.mylist)-1, ascending)
				else:
					sorting_algorithm_generator=sorting_algorithm(draw_info, ascending)
			elif event.key == pygame.K_a and not sorting:
				ascending=True
			elif event.key == pygame.K_d and not sorting:
				ascending=False
			elif event.key == pygame.K_b and not sorting:
				sorting_algorithm=bubble_sort
				sorting_algo_name="Bubble Sort"
			elif event.key == pygame.K_i and not sorting:
				sorting_algorithm=insertion_sort
				sorting_algo_name="Insertion Sort"
			elif event.key == pygame.K_m and not sorting:
				sorting_algorithm=merge_sort
				sorting_algo_name="Merge Sort"
			elif event.key == pygame.K_q and not sorting:
				sorting_algorithm=quick_sort
				sorting_algo_name="Quick Sort"
			elif event.key == pygame.K_h and not sorting:
				sorting_algorithm=heap_sort
				sorting_algo_name="Heap Sort"

	pygame.quit()

if __name__ == "__main__":
	main()
