import java.util.HashMap;
import java.util.PriorityQueue;
import java.util.Queue;

public class Solution {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		int n = 3; // meaning 3 cities or vertices
		int src = 0; // starting from city 0 or vertex 0
		int K = 0; // can have at most k stops during the flight
		int dst = 2; // our destination is city 2 or vertex 2

		// A flight goes from city 0 to 1 with a price of 100
		// A flight goes from city 1 to 2 with a price of 100
		// A flight goes directly from city 0 to 2 with a price of 500
		int[][] flights = { { 0, 1, 100 }, { 1, 2, 100 }, { 0, 2, 500 } };

		int result = findCheapestPrice(n, flights, src, dst, K);

		System.out.println(result);

	}

	public static int findCheapestPrice(int n, int[][] flights, int src, int dst, int K) {

		// calling a private helper method to build my graph from 2D array flights
		HashMap<Integer, HashMap<Integer, Integer>> myGraph = buildGraph(flights);

		// each object in my priority queue is an integer array
		// the ordering will be based on price which is at index 0 in my array
		Queue<int[]> myQueue = new PriorityQueue<int[]>((a, b) -> (Integer.compare(a[0], b[0])));

		// assume total price to get to destination is 0 initially
		// the second element in the array is the source city
		myQueue.add(new int[] { 0, src, K + 1 }); // adding array to my priority queue

		// while my Queue is not empty
		while (!myQueue.isEmpty()) {
			// get the array at the top of the priority queue
			int[] topArray = myQueue.remove();
			// total price from source is the first element in my array
			int totalPrice = topArray[0];
			// current city is at index 1 in my array
			int city = topArray[1];
			// number of stops is at index 2
			int stops = topArray[2];

			// if we have reached the destination
			if (city == dst) {
				return totalPrice;
			}

			// if we have not run out of stops
			if (stops > 0) {
				// Returns the value to which the specified key is mapped
				// get all cities accessible from your current city and their respective prices
				HashMap<Integer, Integer> myMap = myGraph.getOrDefault(city, new HashMap<>());

				// for all the cities accessible from your current city
				for (int key : myMap.keySet()) {
					// get the total price it takes to get to that city
					// store that total price, that city and the number of stops left in the
					// priority queue
					myQueue.add(new int[] { totalPrice + myMap.get(key), key, stops - 1 });
				}
			}

		}
		
		//  return -1 if there is no path  given the specified conditions 
		return -1;
	}

	private static HashMap<Integer, HashMap<Integer, Integer>> buildGraph(int[][] flights) {

		HashMap<Integer, HashMap<Integer, Integer>> myGraph = new HashMap<>();

		// { { 0, 1, 100 }, { 1, 2, 100 }, { 0, 2, 500 } };
		
		// for each 1D array in flights
		for (int[] array : flights) { // for first iteration array will be {0, 1, 100}

			// if my graph doesn't already contain that city
			if (!myGraph.containsKey(array[0])) {
				// put that city in the graph and create a new HashMap
				// to store destination city and price
				myGraph.put(array[0], new HashMap<>());
			}

			// array[0] is the starting city
			// array[1] is the destination city
			// array[2] is the price to reach that city
			myGraph.get(array[0]).put(array[1], array[2]);
		}

		return myGraph;

	}

}
