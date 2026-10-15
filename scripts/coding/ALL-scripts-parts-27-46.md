# LeetCode, Line by Line - scripts for Parts 27-46

Problems reported most often in the last six months at Meta, Apple, Google, Netflix (and Anthropic) in a third-party snapshot of LeetCode company tags dated 12 July 2026. Every solution below was run against a brute force; every figure in the scripts was computed.


---

## Part 27 - Maximum Subarray (LeetCode 53) - 505 words, about 2:53

Reported at: Meta, Apple, Google

```
Today, LeetCode problem fifty three. Maximum Subarray.

Here is the plan. Walk through the numbers once. At each number, keep the best sum of a stretch that ends right here. That is either the number alone, or the number added to the best stretch that ended just before. Remember the biggest value we ever see.

The numbers are two, minus five, three, four, minus one, two. A subarray is a stretch of neighbouring numbers. We want the largest sum any stretch can have.

The direct way tries every start and every end, and adds up the numbers. Six numbers have twenty one stretches. A thousand numbers have about half a million. Even with a running total for each start, that is O of n squared. The bottleneck is that the stretches overlap almost completely, and each one is summed again as if the others never existed.

Here is what removes it. Stand on one number, and ask: should the stretch ending here reach back, or start fresh? Reaching back only helps if the stretch behind us adds something. If the stretch behind us sums to less than zero, it only drags us down, so we drop it and start fresh at this number. This idea is known as Kadane's algorithm.

Now the code. It has two parts.

First, two variables, cur and best. Both start as the first number. Cur is the best sum of a stretch ending at the current number. Best is the best sum we have seen anywhere.

Second, a loop over the remaining numbers. Cur becomes the larger of two things: the number alone, or cur plus the number. Then best becomes the larger of best and cur. At the end, we return best.

Now run it. Cur and best both start at two.

Minus five. Reaching back gives two minus five, which is minus three. Alone, it is minus five. Minus three wins. Cur is minus three, and best stays two.

Three. Reaching back gives minus three plus three, which is zero. Alone, it is three. Alone wins, because the stretch behind us was negative. We start fresh. Cur is three, and best becomes three.

Four. Reaching back gives seven. Cur is seven, and so is best.

Minus one. Reaching back gives six. Cur is six, and best stays seven.

Two. Reaching back gives eight. Cur is eight, and best becomes eight.

We return eight.

To check it: three, plus four, minus one, plus two, is eight. Adding the two and the minus five in front would only lower it. And trying all twenty one stretches finds nothing bigger than eight.

There is one pass, so the time is O of n. Only two variables are kept, so the space is O of one. The direct way was O of n squared.

So that is Maximum Subarray. A stretch is worth extending only while it is adding something. The moment it goes negative, start fresh.

Follow for more if you want to really understand the problems interviews ask. Code included.
```


---

## Part 28 - Subarray Sum Equals K (LeetCode 560) - 544 words, about 3:07

Reported at: Meta, Apple, Google, Amazon, Microsoft

```
A sliding window finds subarray sums easily, until the numbers can be negative. Today, LeetCode problem five hundred sixty. Subarray Sum Equals K.

Here is the plan. Keep a running total from the start. The sum of any stretch is the difference between two of those totals. So at each position, we ask one question: how many earlier totals are exactly k below the current one? A hash map answers it in one step.

The numbers are one, minus one, one, two. K is two. We want how many stretches of neighbouring numbers add up to exactly two.

First, why not a window. With only positive numbers, growing a window always raises its sum, so we know when to shrink it. A negative number breaks that. Growing the window can lower the sum, so the window can never tell which way to move.

The direct way tries every start, and extends it to the right, adding as it goes. Four numbers have ten stretches. A thousand numbers have about half a million. That is O of n squared. The bottleneck is that every start adds up the same numbers again.

Now the running total. Before any number, it is zero. After the numbers it reads one, zero, one, three. A stretch sums to k exactly when the total at its end, minus the total just before its start, is k. So at each position, we look for earlier totals equal to the current total minus k.

And the same total can appear more than once. Here zero appears twice, and one appears twice. So the map must store how many times each total has appeared.

Now the code. It has three parts.

First, seen is a map from a total to how many times it has appeared. It starts with zero seen once, which is the empty start. Total and count start at zero.

Second, the loop. Add the number to the total. Then add to count however many times total minus k has been seen.

Third, record the new total in the map, one more time. We look up first and store second, so a stretch can never be made of nothing. Then we return count.

Now run it. Seen holds zero once.

The first number is one. Total is one. We need minus one, never seen. Store one.

Minus one. Total is zero. We need minus two, never seen. Zero has now been seen twice.

One. Total is one. We need minus one, never seen. One has now been seen twice.

Two. Total is three. We need one, and one has been seen twice. Count jumps by two. Count is two.

We return two.

To check it: minus one, plus one, plus two is two. And the number two alone is two. Trying all ten stretches finds exactly these.

One pass, with one map lookup per number: O of n time. The map holds up to one entry per total: O of n space. We paid memory to get rid of the repeated adding.

So that is Subarray Sum Equals K. A stretch is the gap between two running totals, so counting stretches means counting earlier totals.

Follow for more if you want to really understand the problems interviews ask. Code included.
```


---

## Part 29 - Find First and Last Position of Element in Sorted Array (LeetCode 34) - 603 words, about 3:27

Reported at: Meta, Apple, Google, Amazon, Microsoft

```
Today, LeetCode problem thirty four. Find First and Last Position of Element in Sorted Array.

Here is the plan. Write one small binary search that finds the first position where a number is not smaller than x. Use it twice. The first position of the target is the answer for the target. The last position of the target is one before the answer for the next number up.

The array is five, seven, seven, eight, eight, eight, ten. The target is eight. We return the first and last index where eight sits, or minus one and minus one if it is not there.

The direct way scans from the left until it hits eight, then scans from the right. That is O of n. A plain binary search finds some eight quickly, but not necessarily the first or the last. If a million numbers were all eight, we would have to walk outwards, and that is O of n again. The bottleneck is that finding any eight is not enough. We need the edges of the run.

So change the question. Not where is eight, but where is the first number that is not smaller than eight. In a sorted array, that is the left edge of the eights. And the first number not smaller than nine is just past the right edge. This small search is called a lower bound.

Now the code. It has two parts.

First, a helper called lower. Lo starts at zero, and hi starts at the length, one past the end, so the answer can be that spot. While lo is below hi, find the middle. If the number at mid is smaller than x, the answer is to the right, so lo moves to mid plus one. Otherwise mid might itself be the answer, so hi moves to mid. When they meet, that is the answer.

Second, the main part. First is lower of the target. If that is past the end, or the number there is not the target, the target is missing, and we return minus one and minus one. Otherwise, last is lower of target plus one, minus one.

Now run it. Lower of eight. Lo is zero, hi is seven. Mid is three, and the number is eight. Not smaller, so hi moves to three.

Mid is one, and the number is seven. Smaller, so lo moves to two. Mid is two, and the number is seven. Smaller, so lo moves to three. Lo and hi are both three. First is three.

Now lower of nine. Mid is three, and the number is eight, which is smaller than nine, so lo moves to four. Mid is five, and the number is eight, smaller again, so lo moves to six. Mid is six, and the number is ten. Not smaller, so hi moves to six. The answer is six. Minus one, and last is five.

We return three and five.

To check it: indexes three, four, and five hold eights. Index two holds a seven, and index six holds a ten. If the target were six, lower would return index one, where the number is seven. That is not six, so we would return minus one and minus one.

Each search halves the range: O of log n. Only a few variables: O of one space. The direct way was O of n.

So that is Find First and Last Position. Do not search for the number. Search for the edge, the first spot not smaller than it.

Follow for more if you want to really understand the problems interviews ask. Code included.
```


---

## Part 30 - Koko Eating Bananas (LeetCode 875) - 573 words, about 3:16

Reported at: Meta, Apple, Google, Amazon, Microsoft

```
Today, LeetCode problem eight hundred seventy five. Koko Eating Bananas.

Here is the plan. Do not search the piles. Search the speed. For any speed, counting the hours it needs is easy. And a faster speed never needs more hours. So the speeds split into too slow, then fast enough. We binary search for the first fast enough one.

There are four piles of bananas: three, six, seven, and eleven. Koko eats at a speed of k bananas an hour. Each hour she picks one pile, and eats up to k from it. If the pile has fewer, she finishes it and waits out the hour. She has eight hours. We want the smallest speed that finishes in time.

The direct way tries speed one, then two, then three, and counts the hours for each. Speed one takes twenty seven hours. Speed two takes fifteen. Speed three takes ten. Speed four takes eight, and that works. For huge piles, that is a huge number of speeds to try. The bottleneck is that we test every speed, even though hours only ever go down as the speed goes up.

So the speeds look like this: too slow, too slow, too slow, fine, fine, fine. One cut point. Finding a cut point in a sorted list of answers is exactly what binary search is for.

Now the code. It has three parts.

First, the range. Lo is one, the slowest speed that makes sense. Hi is the biggest pile, because at that speed every pile takes one hour, and no speed above it can be better.

Second, the loop, while lo is below hi. Mid is a speed to test. To count its hours, go through the piles, and add each pile plus mid minus one, divided by mid, rounded down. That is a way of dividing and rounding up. A pile of seven at speed three needs three hours, not two and a bit.

Third, the decision. If the hours are at most h, this speed works, but a slower one might too, so hi moves to mid. Otherwise this speed is too slow, so lo moves to mid plus one. When they meet, we return lo.

Now run it. Lo is one, hi is eleven. Mid is six. The piles take one, one, two, and two hours. Six hours is within eight, so hi moves to six.

Lo is one, hi is six. Mid is three. One, two, three, four. Ten hours is too many, so lo moves to four.

Lo is four, hi is six. Mid is five. One, two, two, three. Eight hours works, so hi moves to five.

Lo is four, hi is five. Mid is four. One, two, two, three. Eight hours works, so hi moves to four.

Lo and hi are both four. We return four.

To check it: speed three needs ten hours, which is too many. Speed four needs exactly eight.

The search takes about log of the biggest pile steps. Each step goes through all n piles. So the time is O of n times log of the biggest pile. Only a few variables: O of one space. Trying every speed would cost n times the biggest pile.

So that is Koko Eating Bananas. When the answer is a number, and larger numbers only get easier, binary search the answer.

Follow for more if you want to really understand the problems interviews ask. Code included.
```


---

## Part 31 - Longest Palindromic Substring (LeetCode 5) - 537 words, about 3:04

Reported at: Meta, Apple, Google, Amazon, Microsoft

```
Today, LeetCode problem five. Longest Palindromic Substring.

Here is the plan. Every palindrome has a centre, and reads the same outwards in both directions. So pick a centre, and grow outwards while the two sides match. Try every centre, and keep the longest result.

The string is a, b, b, c, b. We want the longest stretch that reads the same forwards and backwards.

The direct way checks every substring to see if it is a palindrome. Five letters have fifteen substrings, and each check reads its letters again. For n letters, that is O of n cubed. The bottleneck is that a long palindrome contains shorter palindromes, and each check starts from nothing and proves it all over again.

Now notice how a palindrome is built. If the centre is a palindrome, and the letters just outside it match, then the bigger one is a palindrome too. So we never need to start from the outside. We start from the middle, and grow.

A centre comes in two kinds. A palindrome with an odd length is centred on one letter, like b, c, b. A palindrome with an even length is centred between two letters, like b, b. For five letters, that is five letter centres, and four between-letter centres. Nine in total.

Now the code. It has two parts.

First, a helper called expand. It takes a left and a right position. While both are inside the string, and the two letters match, left steps one left, and right steps one right. When it stops, those positions have gone one step too far on each side, so the palindrome is the text from left plus one up to right. If that is longer than best, it replaces best.

Second, the loop. For every position i, call expand from i and i, for odd palindromes. Then call expand from i and i plus one, for even ones. At the end, we return best.

Now run it. Position zero. The letter a alone is a palindrome of length one. Best is a. Between a and b, the letters differ, so nothing grows.

Position one. The letter b alone is length one, not longer. Between the two b's, the letters match. Then a against c differs. We found b, b. Length two. Best is b, b.

Position two. The b alone is length one. Between b and c, nothing.

Position three. The c matches itself. Its neighbours are both b, so they match. Next, the left side is a, and the right side is past the end, so it stops. We found b, c, b. Length three. Best is b, c, b.

Position four. The b alone is length one. Nothing else.

We return b, c, b.

To check it: b, c, b reads the same backwards. And trying all fifteen substrings finds nothing longer.

There are n centres, and each grows at most n steps: O of n squared time. Only a few variables: O of one extra space. The direct way was O of n cubed.

So that is Longest Palindromic Substring. Do not test substrings. Grow palindromes from their centres.

Follow for more if you want to really understand the problems interviews ask. Code included.
```


---

## Part 32 - Kth Largest Element in an Array (LeetCode 215) - 499 words, about 2:51

Reported at: Meta, Apple, Google, Amazon, Microsoft

```
Today, LeetCode problem two hundred fifteen. Kth Largest Element in an Array.

Here is the plan. We only care about the biggest k numbers. So keep a small collection that holds just those, and always lets us throw out its smallest member. Once we have seen every number, the smallest member of the collection is the answer.

The numbers are three, two, one, five, six, four. K is two. We want the second largest number, counting duplicates as separate numbers.

The direct way sorts the whole array from big to small, and picks the number at position k. That is O of n log n. The bottleneck is that sorting puts every number in order, but we only wanted the top two. Almost all of that ordering work is thrown away.

So we need a collection that is good at one thing: telling us its smallest member, and removing it, quickly. That is a min heap. Looking at the smallest takes one step. Adding or removing takes about log of its size.

Why the smallest? Because the collection holds the k biggest so far. When a new number arrives and the collection is too big, the one that must leave is the smallest of them. It can never be the kth largest of the top group.

Now the code. It has two parts.

First, an empty list called heap. Python's heapq module turns a plain list into a min heap.

Second, a loop over the numbers. Push the number into the heap. If the heap now holds more than k numbers, pop the smallest one out. After the loop, the smallest number in the heap, heap of zero, is the kth largest. We return it.

Now run it. K is two.

Three goes in. The heap holds three.

Two goes in. The heap holds two and three. That is two numbers, so nothing leaves.

One goes in. Now there are three numbers, one too many. The smallest, one, leaves. The heap holds two and three.

Five goes in. The smallest, two, leaves. The heap holds three and five.

Six goes in. The smallest, three, leaves. The heap holds five and six.

Four goes in. It is the smallest, so it leaves straight away. The heap still holds five and six.

The smallest in the heap is five. We return five.

To check it: sorted from big to small, the numbers are six, five, four, three, two, one. The second one is five.

Every number costs one push and at most one pop, each about log of k: O of n log k time. The heap never holds more than k plus one numbers: O of k space. When k is small, that beats sorting everything.

So that is Kth Largest Element. To find the top k, keep a small heap of the best so far, and let the smallest of them be the doorkeeper.

Follow for more if you want to really understand the problems interviews ask. Code included.
```


---

## Part 33 - Merge k Sorted Lists (LeetCode 23) - 564 words, about 3:13

Reported at: Meta, Apple, Google, Amazon

```
Today, LeetCode problem twenty three. Merge k Sorted Lists.

Here is the plan. In each sorted list, only the front node matters, because it is the smallest one left in that list. So the next number in the answer is always the smallest of the fronts. Keep the fronts in a min heap. Take the smallest, add it to the answer, and put its next node into the heap.

There are three sorted linked lists. One, four, five. One, three, four. Two, six. We want one sorted list with all eight nodes.

The direct way looks at the front of every list, picks the smallest, and moves on. That is k comparisons for every node we place. With n nodes in total, that is O of n times k. The bottleneck is that after one pick, only one front has changed, but we compare all of them again.

So we want a collection that remembers the smallest front, and is cheap to update when one front changes. That is a min heap. Taking the smallest, and adding a new front, each cost about log of its size. And the heap never holds more than one front per list.

Now the code. It has three parts.

First, fill the heap. For each list that is not empty, push a tuple holding three things: the value of its front node, the list's index, and the node itself. The heap orders tuples by their first item. The index sits second for a reason. If two values are equal, Python moves on to the next item, and nodes cannot be compared. The index always settles the tie.

Second, a dummy node, and a tail that points at it. The answer grows behind the tail.

Third, the loop, while the heap is not empty. Pop the smallest. Attach that node to the tail, and move the tail onto it. If that node has a next node, push the next node into the heap. At the end, the answer starts at dummy dot next.

Now run it. The heap holds the three fronts: one from the first list, one from the second, and two from the third.

Pop the one from the first list. Its next node, four, goes in.

Pop the one from the second list. Its next node, three, goes in.

Pop the two. Its next node, six, goes in.

Pop the three. Its next node, four, goes in. The heap holds four, four, and six.

Pop the four from the first list. Its next node, five, goes in. Pop the four from the second list. That list has no next node, so nothing goes in.

Pop the five. That list is finished too. Pop the six. The heap is empty.

The answer is one, one, two, three, four, four, five, six.

To check it: that is all eight numbers, in order. Every node was attached exactly once.

Every node is pushed once and popped once, and the heap holds at most k nodes: O of n log k time. The heap itself takes O of k space, since we reuse the original nodes. The direct way was O of n times k.

So that is Merge k Sorted Lists. Only the fronts matter, and a heap always knows which front is smallest.

Follow for more if you want to really understand the problems interviews ask. Code included.
```


---

## Part 34 - Meeting Rooms II (LeetCode 253) - 568 words, about 3:15

Reported at: Meta, Apple, Google, Amazon, Microsoft

```
Today, LeetCode problem two hundred fifty three. Meeting Rooms Two.

Here is the plan. Sort the meetings by start time. Keep the end times of the meetings that are using a room. When a new meeting starts, look at the room that frees up first. If it is already free, reuse it. If not, open a new room. At the end, the number of rooms in use is the answer.

There are four meetings, given as a start and an end. Zero to thirty. Five to ten. Fifteen to twenty. Eighteen to twenty five. We want the fewest rooms that fit all of them with no overlap.

The direct way takes every meeting, and counts how many other meetings are running at its start time. The largest count is the answer. With n meetings, that is O of n squared. The bottleneck is that for every meeting we look through all the others, when only one thing matters: which room becomes free first.

That one thing is the smallest end time among the busy rooms. If any room is free for the new meeting, the room that finishes earliest surely is. So a min heap of end times is all we need.

Now the code. It has three parts.

First, sort the meetings. Since each meeting is a start and an end, sorting puts them by start time.

Second, the heap, called ends. It holds the end time of the last meeting in each room.

Third, the loop. For each meeting, if the heap is not empty, and its smallest end time is at or before this meeting's start, that room is free, so we pop its end time. Then, whether we reused a room or not, we push this meeting's end time. The heap now has one entry per room. At the end, we return its size.

Now run it. The sorted meetings are the same four.

Zero to thirty. The heap is empty, so a new room is opened. The heap holds thirty.

Five to ten. The smallest end is thirty, which is after five. That room is busy. A second room opens. The heap holds ten and thirty.

Fifteen to twenty. The smallest end is ten, which is before fifteen. That room is free. We take it over. Ten leaves, and twenty goes in. The heap holds twenty and thirty. Still two rooms.

Eighteen to twenty five. The smallest end is twenty, which is after eighteen. Busy. A third room opens. The heap holds twenty, twenty five, and thirty.

We return three.

To check it: at time eighteen, the meetings zero to thirty, fifteen to twenty, and eighteen to twenty five are all running at once. Three at the same time needs three rooms.

If one meeting ends at the exact moment another starts, they can share a room. That is why the test says at or before.

Sorting costs O of n log n, and each meeting does one push and at most one pop, also about log n. Time is O of n log n. The heap holds up to n end times: O of n space. The direct way was O of n squared.

So that is Meeting Rooms Two. The next free room is always the one that ends first, and a heap finds it instantly.

Follow for more if you want to really understand the problems interviews ask. Code included.
```


---

## Part 35 - Course Schedule II (LeetCode 210) - 551 words, about 3:09

Reported at: Meta, Apple, Google, Netflix, Amazon, Microsoft (the only problem in all six lists)

```
Today, LeetCode problem two hundred ten. Course Schedule Two.

Here is the plan. For every course, count how many prerequisites it still needs. Take any course that needs none, and write it down. Taking it lowers the count of every course that was waiting on it. The order we write down is a valid schedule. If we get stuck before writing down every course, there is a cycle, and no schedule exists.

There are four courses, zero to three. Course one needs course zero. Course two needs course zero. Course three needs both one and two. In the earlier problem, Course Schedule, we only had to say whether all courses could be taken. Here we must return an order that works, or an empty list if none does.

The direct way scans all the courses again and again, looking for one whose prerequisites are all taken. Each scan costs a pass over everything, and there can be as many scans as courses. The bottleneck is rescanning courses whose situation has not changed.

But a course only becomes ready at one moment: when its last prerequisite is taken. So instead of rescanning, keep a count of missing prerequisites for each course, and a queue of the courses whose count is zero. This is called a topological sort.

Now the code. It has four parts.

First, build the graph. After maps each course to the courses that depend on it. Needs counts each course's missing prerequisites.

Second, every course whose count is zero goes into the queue.

Third, the loop. Take a course from the queue, and add it to the order list. For each course that depends on it, lower its count by one. If the count reaches zero, that course joins the queue.

Fourth, the result. If the order holds all n courses, we return it. Otherwise, we return an empty list.

Now run it. The counts are zero, one, one, and two. Only course zero is ready.

Take zero. The order is zero. Courses one and two each lose a requirement. Both reach zero, and join the queue.

Take one. The order is zero, one. Course three goes from two to one. Not ready yet.

Take two. The order is zero, one, two. Course three reaches zero, and joins the queue.

Take three. The order is zero, one, two, three. Four courses out of four, so we return that order.

To check it: course one and course two come after zero, and course three comes after both. Every course sits after its prerequisites. Zero, two, one, three would also work, and any valid order is accepted.

Now the failing case. If course zero needed course one, and course one needed course zero, neither count could ever reach zero. The queue starts empty. The order stays empty, which is shorter than two, so we return an empty list.

Every course and every prerequisite is handled once: O of courses plus prerequisites, in time and in space. The direct way could rescan the whole graph once for every course.

So that is Course Schedule Two. Take what is ready, let each course unlock what depends on it, and the order you took them in is the schedule.

Follow for more if you want to really understand the problems interviews ask. Code included.
```


---

## Part 36 - Word Ladder (LeetCode 127) - 659 words, about 3:46

Reported at: Meta, Apple, Google, Amazon, Microsoft

```
Today, LeetCode problem one hundred twenty seven. Word Ladder.

Here is the plan. Think of every word as a point, with a line to every word that differs by one letter. The fewest steps from the start word to the end word is a shortest path. A search that spreads out one step at a time, called breadth first search, finds it. To find a word's neighbours, do not compare it with the whole list. Change each letter to each of the twenty six letters, and check if the result is a real word.

The start word is hit. The end word is cog. The word list is hot, dot, dog, lot, log, cog. Each step changes one letter, and every word along the way must be in the list. We return how many words are in the shortest chain, counting hit and cog. If there is no chain, we return zero.

The direct way compares every pair of words, to build the lines. Hit and the six words make seven, which is twenty one pairs. For ten thousand words, that is about fifty million pairs. The bottleneck is that we ask every word about every other word, when each word really has only a handful of neighbours.

So flip it. A word of length L has L positions, and twenty six letters to try in each. Those are all the neighbours it could possibly have. We make each candidate, and look it up in a set, which takes one step.

And why breadth first? It visits words in rings. First everything one step away, then everything two steps away. So the first time we reach a word is by the shortest route.

Now the code. It has three parts.

First, put the words in a set for fast lookup. If the end word is not in the set, no chain can finish, so we return zero. The queue starts with the start word, and a count of one, since the chain already holds one word.

Second, the loop. Take a word and its count from the queue. If it is the end word, return the count.

Third, the neighbours. For every position in the word, and every letter, build a candidate with that one letter swapped. If the candidate is in the set, remove it from the set, and queue it with the count plus one. Removing it means we can never queue it twice. If the queue runs dry, we return zero.

Now run it. Hit, with a count of one. Changing its first letter finds nothing. Changing its middle letter to o gives hot. It is in the set, so it is queued with two.

Take hot. Changing its first letter finds dot, and lot. Both are queued with three.

Take dot. Changing its last letter finds dog. Queued with four.

Take lot. Changing its last letter finds log. Queued with four.

Take dog. Changing its first letter to c gives cog. Queued with five.

Take log. Its neighbours have already been used. Nothing new.

Take cog. It is the end word. We return five.

To check it: hit, hot, dot, dog, cog. Each word differs from the one before by exactly one letter. That is five words. And if cog were not in the list, we would return zero straight away.

Each word enters the queue at most once. For each, we try length times twenty six candidates, and each candidate costs a string of length L to build. Time is O of n times L squared, with the twenty six as a constant. The set and the queue take O of n times L space. The direct way was O of n squared times L.

So that is Word Ladder. Do not compare words with each other. Generate the neighbours, and let a breadth first search count the steps.

Follow for more if you want to really understand the problems interviews ask. Code included.
```


---

## Part 37 - Minimum Remove to Make Valid Parentheses (LeetCode 1249) - 514 words, about 2:56

Reported at: Meta (top of its list), Google

```
Today, LeetCode problem one thousand two hundred forty nine. Minimum Remove to Make Valid Parentheses.

Here is the plan. Walk through the string once, with a stack that holds the positions of open brackets still waiting for a partner. A closing bracket with nothing waiting can never be matched, so mark it for removal. When the walk ends, any open bracket still waiting never got a partner, so mark those too. Everything left is a valid string.

The string is a, close bracket, b, open bracket, c, close bracket, d, open bracket. Brackets here means round parentheses. We remove as few brackets as possible, so that the brackets are valid. Letters are never removed.

The direct way tries removing every possible set of characters, and keeps the smallest removal that leaves a valid string. Eight characters have two hundred fifty six sets, and the count doubles with every extra character. The bottleneck is that we guess which brackets to remove, when the string itself can tell us.

And it can. A closing bracket is hopeless if no open bracket is waiting before it. An open bracket is hopeless if nothing closed it by the end. Those are the only two ways a bracket can fail.

Now the code. It has three parts.

First, turn the string into a list of characters, because strings cannot be changed in place. We will blank out the bad ones. Then make an empty stack.

Second, the loop over each position. If the character is an open bracket, push its position on the stack. If it is a closing bracket, then, if the stack has an open bracket waiting, pop it, because they are partners. If the stack is empty, there is nothing to match, so blank this character.

Third, after the loop, every position still on the stack is an open bracket that never found a partner. Blank them all. Then join the list back into a string.

Now run it. Position zero is a letter. Nothing happens.

Position one is a closing bracket. The stack is empty. Blank it.

Position two is a letter. Position three is an open bracket. The stack holds three.

Position four is a letter. Position five is a closing bracket. The stack has three, so they are partners. Pop it.

Position six is a letter. Position seven is an open bracket. The stack holds seven.

The loop ends. Seven is still on the stack. It never closed. Blank it.

Joining what is left gives a, b, open bracket, c, close bracket, d.

To check it: the one bracket pair is matched. We removed exactly two brackets, and trying all two hundred fifty six sets confirms that no valid string needs fewer removals.

One pass, one stack, one list: O of n time, and O of n space. The direct way was exponential.

So that is Minimum Remove to Make Valid Parentheses. Do not guess what to remove. A stack tells you which brackets never found a partner.

Follow for more if you want to really understand the problems interviews ask. Code included.
```


---

## Part 38 - Basic Calculator II (LeetCode 227) - 611 words, about 3:29

Reported at: Apple (top of its list), Meta

```
Today, LeetCode problem two hundred twenty seven. Basic Calculator Two.

Here is the plan. Times and divide bind tighter than plus and minus. So treat the expression as a sum of terms. Keep a stack of terms. A plus or minus starts a new term, so we push the number. A times or divide changes the term on top, so we combine the number with it right away. At the end, the answer is the sum of the stack.

The expression is three, plus, twelve, times, two, minus, eight, divide, four. It has only whole numbers and four operators. Division throws away the fraction, rounding toward zero. We return the value.

What makes this hard is the order of things. An operator comes before the number it applies to. But we only know a number is finished when we reach the next operator, or the end. So we cannot act when we see an operator. We must remember the operator that came before the number, and act when the number is complete.

Reading the digits is the first part of that. A number can have several digits. For each new digit, the number so far is multiplied by ten, and the digit is added. Twelve is one, then ten plus two.

Now the code. It has four parts.

First, the setup. Remove the spaces. Make an empty stack. Num is zero. And op, the previous operator, starts as plus. A made up plus in front of the first number is the same as no sign at all.

Second, the loop over each character. If it is a digit, extend num.

Third, when the character is an operator, or it is the very last one, the number is finished. Look at the previous operator. Plus pushes the number. Minus pushes the number made negative. Times pops the top of the stack, and pushes the top times the number. Divide pops the top, and pushes the top divided by the number, with int cutting the fraction toward zero. Then op becomes this character, and num goes back to zero.

Fourth, return the sum of the stack.

Now run it. Three is read. Then the plus ends it. The previous operator is the made up plus, so three is pushed. The stack holds three.

Twelve is read. Then the times ends it. The previous operator is plus, so twelve is pushed. The stack holds three and twelve. The previous operator is now times.

Two is read. The minus ends it. The previous operator is times, so we pop twelve, and push twelve times two. The stack holds three and twenty four. The previous operator is now minus.

Eight is read. The divide ends it. The previous operator is minus, so we push minus eight. The stack holds three, twenty four, and minus eight. The previous operator is now divide.

Four is read, and it is the last character. The previous operator is divide, so we pop minus eight, and push minus eight divided by four. That is minus two. The stack holds three, twenty four, and minus two.

The sum is twenty five.

To check it by hand: twelve times two is twenty four. Eight divided by four is two. Three, plus twenty four, minus two, is twenty five.

One pass over the characters: O of n time. The stack can hold up to one term per number: O of n space.

So that is Basic Calculator Two. Remember the operator before each number, and finish multiplication on the spot. What is left on the stack only needs adding.

Follow for more if you want to really understand the problems interviews ask. Code included.
```


---

## Part 39 - Time Based Key-Value Store (LeetCode 981) - 670 words, about 3:50

Reported at: Netflix, Apple, Meta, Google, Amazon

```
Today, LeetCode problem nine hundred eighty one. Time Based Key-Value Store.

Here is the plan. For each key, keep a list of its values, each with the time it was set. The times only ever go up, so each list is already sorted. To get a value at a time, find the last entry whose time is not after the asked time. That is a binary search.

We build a store with two operations. Set takes a key, a value, and a timestamp. Get takes a key and a timestamp, and returns the value that was set at the latest timestamp that is not after the one asked. If there is none, it returns an empty string.

Our example uses one key, love. At time one, the value is high. At time four, it is low. At time nine, it is peak. Then we ask for the value at time four, at time seven, at time zero, and at time ten.

The direct way keeps the entries for a key in order, and scans them from the start for the last one not after the asked time. With a thousand updates to one key, a single get may touch a thousand entries. That is O of n per get. The bottleneck is that the list is sorted by time, and the scan ignores that.

So use the order. The entries before some point all have times not after the asked time, and the entries after it all have times that are later. Finding that point is a binary search.

Now the code. It has three parts.

First, the constructor. The store is a dictionary, mapping each key to its list of entries.

Second, set. If the key has no list yet, make an empty one. Then append the pair of timestamp and value. The problem promises timestamps for a key only go up, so appending keeps the list sorted.

Third, get. Take the key's list, or an empty list if the key is unknown. Then binary search for the first entry whose timestamp is later than the one asked. Lo starts at zero, and hi at the length. While lo is below hi, find mid. If the entry at mid is not later, the answer lies to the right, so lo moves to mid plus one. Otherwise hi moves to mid. When the search ends, lo is the position of the first later entry. So the entry just before it, at lo minus one, is the answer. If lo is zero, nothing is early enough, and we return an empty string.

Now run it. The list holds time one with high, time four with low, and time nine with peak.

Get at time four. The first later entry is time nine, at position two. So we take position one. Low.

Get at time seven. Mid is one, and its time, four, is not later, so lo moves to two. Mid is two, and its time, nine, is later, so hi moves to two. Lo is two. We take position one. Low again, because nothing was set between four and seven.

Get at time zero. Every entry is later, so lo stays at zero. We return an empty string.

Get at time ten. No entry is later, so lo goes all the way to three. We take position two. Peak.

To check it: at time seven, the latest update at or before it was time four, and that one set low.

Set adds to the end of a list: O of one. Get is one binary search: O of log n for the list of that key. The store holds every value ever set: O of n space. The direct scan was O of n per get.

So that is Time Based Key-Value Store. When data arrives in time order, it is already sorted, and a binary search can look up any moment in the past.

Follow for more if you want to really understand the problems interviews ask. Code included.
```


---

## Part 40 - Design Hit Counter (LeetCode 362) - 586 words, about 3:21

Reported at: Apple (top of its list), Meta, Google

```
Today, LeetCode problem three hundred sixty two. Design Hit Counter.

Here is the plan. Keep the timestamps of hits in a queue, oldest first. When someone asks how many hits happened recently, remove the old ones from the front, and the length of the queue is the answer.

We build a counter with two operations. Hit records a hit at a timestamp, in seconds. Get hits takes a timestamp, and returns how many hits happened in the last three hundred seconds. Timestamps never go backwards.

Our example. Hits arrive at times one, two, and three. We ask at time four. Then a hit arrives at time three hundred. We ask at time three hundred, and then at time three hundred one.

The direct way stores every hit forever, in a list. To answer, it counts the hits that are inside the window. With a million hits stored, every question reads a million entries, and the list never stops growing. The bottleneck is that time only moves forward. A hit that has fallen out of the window will never count again, yet we keep storing it, and keep checking it.

So throw the old hits away. They are also the oldest, so they sit at the front of a queue. We only ever need to look at the front.

Now the code. It has three parts.

First, the constructor. Hits is an empty queue.

Second, hit. Append the timestamp to the back. Timestamps never go down, so the queue stays in order.

Third, get hits. While the queue is not empty, and the oldest timestamp is at or before the asked time minus three hundred, remove it from the front. Then return the length of the queue.

The test says at or before for a reason. The window is the last three hundred seconds, so at time three hundred one it covers time two up to three hundred one. A hit at time one is outside.

Now run it. Three hits go in: one, two, and three.

Get hits at time four. Four minus three hundred is far below zero. The oldest hit, time one, is not older than that. Nothing leaves. The length is three.

A hit arrives at time three hundred. The queue holds one, two, three, and three hundred.

Get hits at time three hundred. Three hundred minus three hundred is zero. The oldest hit, time one, is not at or before zero. Nothing leaves. The length is four.

Get hits at time three hundred one. Three hundred one minus three hundred is one. The oldest hit, time one, is at or before one. It leaves. The next oldest, time two, is after one. We stop. The length is three.

To check it: at time three hundred one, the window covers two to three hundred one. The hits at two, three, and three hundred are inside. That is three.

A hit is an append: O of one. Every timestamp is removed at most once, so across all calls a get is O of one on average. The queue holds the hits inside the window: O of n space, where n is the number of hits in the last three hundred seconds. The direct way was O of n per question, with memory that grew forever.

So that is Design Hit Counter. Time only moves forward, so throw old events away from the front, and never look at them again.

Follow for more if you want to really understand the problems interviews ask. Code included.
```


---

## Part 41 - String to Integer (atoi) (LeetCode 8) - 616 words, about 3:31

Reported at: Netflix, Meta, Google, Amazon, Microsoft

```
Today, LeetCode problem eight. String to Integer, also called atoi.

Here is the plan. There is no clever trick here. The problem is a list of rules, and the skill is doing them in the right order. Skip the spaces at the front. Read an optional sign. Read digits until something that is not a digit. Apply the sign, and keep the result inside the range of a thirty two bit integer.

The string is two spaces, a minus sign, the digits nine one two eight three four seven two three three two, a space, and then the letters a and b. We return the integer the string starts with.

What makes this hard is not the work. It is the edge cases. Spaces can come first. The sign is optional. Anything after the digits is ignored. If there are no digits at all, the answer is zero. And a number too big for thirty two bits must be cut back to the nearest limit. Those limits are minus two billion, one hundred forty seven million, four hundred eighty three thousand, six hundred forty eight, and two billion, one hundred forty seven million, four hundred eighty three thousand, six hundred forty seven.

Now the code. It has four parts.

First, an index i, which marks where we are in the string. While the character at i is a space, move i forward.

Second, the sign. Start with sign set to one. If the character at i is a plus or a minus, set sign to minus one for a minus, and step past it.

Third, the digits. Result starts at zero. While we are inside the string, and the character at i is a digit from zero to nine, result becomes result times ten, plus that digit. Then i moves forward. The loop stops at the first character that is not a digit, or at the end.

Fourth, the finish. Multiply by the sign. Then clamp: take the smaller of the result and the top limit, and then the larger of that and the bottom limit. Python never overflows, so we can clamp at the end. In a language with fixed size integers, the check has to happen before each digit is added.

Now run it. The index skips the two spaces, and stands on the minus sign. The sign is minus one, and the index moves past it.

Now the digits. Nine. Ninety one. Nine hundred twelve. Each new digit moves the result one place left, and adds itself. After eleven digits, the result is ninety one billion, two hundred eighty three million, four hundred seventy two thousand, three hundred thirty two.

The next character is a space, which is not a digit. The loop stops. The letters a and b are never read.

Times minus one, the result is minus ninety one billion and change. That is below the bottom limit. So the clamp returns the bottom limit, minus two billion, one hundred forty seven million, four hundred eighty three thousand, six hundred forty eight.

To check the edge cases: the string words and nine eight seven gives zero, because the first character is not a digit. A plain plus one gives one. And minus, then a leading zero, then four two, gives minus forty two, because leading zeros do nothing.

One pass over the string: O of n time. A few variables: O of one space.

So that is String to Integer. A problem made of rules is solved by doing the rules one at a time, in order, and writing down which edge case each line covers.

Follow for more if you want to really understand the problems interviews ask. Code included.
```


---

## Part 42 - Valid Word Abbreviation (LeetCode 408) - 527 words, about 3:01

Reported at: Meta (top of its list)

```
Today, LeetCode problem four hundred eight. Valid Word Abbreviation.

Here is the plan. Put one pointer on the word, and one on the abbreviation. A letter in the abbreviation must match the letter in the word, and both pointers step forward. A number in the abbreviation tells the word pointer to jump that many letters. If both pointers land exactly at the end together, the abbreviation is valid.

The word is substitution, which has twelve letters. The abbreviation is s, one, zero, n. Is it a valid abbreviation of the word? A number stands for that many letters, skipped. A number may have several digits, and it may never start with a zero.

What makes this tricky is the numbers. One digit and two digits are read differently, one zero is not the number ten, and a number can jump past the end of the word. So we must read the whole number, check it, and only then jump.

Now the code. It has three parts.

First, the setup. M and n are the two lengths. I is the pointer in the word. J is the pointer in the abbreviation. Both start at zero.

Second, a digit. While both pointers are inside, look at the abbreviation. If it is a digit, and it is a zero, we return false, because numbers cannot start with a zero. Otherwise read the whole number. While the next characters are digits, the number becomes itself times ten, plus the digit, and j moves forward. Then i jumps ahead by the number.

Third, a letter. It must equal the word's letter at i. If not, we return false. If it does, both pointers move one step.

After the loop, we return whether i reached the end of the word, and j reached the end of the abbreviation. Both, exactly.

Now run it. I is zero, and j is zero. The abbreviation says s. The word says s. A match. Both move to one.

Now the abbreviation says one. A digit, and not a zero. Read the whole number. One, then ten. J moves past both digits, to three. I jumps ahead by ten, from one to eleven.

The abbreviation says n. The word at index eleven is n. A match. I is twelve, and j is four.

The loop ends. Twelve is the length of the word, and four is the length of the abbreviation. Both at the end. We return true.

To check the failures. Write s, zero, one, zero, n, and we return false at the first zero. Write s, eleven, n, and the jump goes to the end of the word, but the letter n is still waiting, so j is not at its end. False. Write s, nine, n, and the jump lands on o, not n. False.

Each pointer only moves forward, so we do one pass: O of m plus n time. A few variables: O of one space.

So that is Valid Word Abbreviation. Read the number completely, jump once, and check at the end that both sides finished together.

Follow for more if you want to really understand the problems interviews ask. Code included.
```


---

## Part 43 - Web Crawler (LeetCode 1236) - 540 words, about 3:05

Reported at: Anthropic (4 problems total on record, all older than six months), also a graph-search staple

```
Today, LeetCode problem one thousand two hundred thirty six. Web Crawler.

Here is the plan. A website is a graph. Pages are the points, and links are the lines between them. Start at the home page, and spread outwards, one step at a time. Keep a record of every page we have seen, so that we never visit one twice. And follow only links that stay on the same host as the start page.

You are given a start page, and a helper that can return the links on any page. Our example has four pages. The home page, on news dot site dot com. The sports page, and the world page, also on news dot site dot com. And one page on other dot com. The home page links to the sports page, and to the other dot com page. The sports page links back to home, and on to the world page. The world page links to the other dot com page, and back to sports. We return every page we can reach that is on news dot site dot com.

What makes this hard is two things. First, links form loops. Sports links back to home. Without memory, we would go round forever. Second, links leave the site. The other dot com page must be ignored, and everything it links to.

Now the code. It has three parts.

First, a small helper called host. It splits the address at the slashes. The third piece is the host name. Domain is the host of the start page.

Second, the memory. Seen is a set that starts holding the start page. The queue also starts with the start page.

Third, the loop. Take a page from the queue. Ask the helper for its links. For each link, if its host is not the domain, or we have already seen it, skip it. Otherwise add it to seen, and to the queue. We mark it seen the moment we queue it, so it can never be queued twice. At the end, we return everything in seen.

Now run it. The queue holds the home page.

Take home. Its first link is sports. Same host, not seen. Add it. Its second link is the other dot com page. A different host. Skip.

Take sports. Its first link is home. Already seen. Skip. Its second link is world. Same host, new. Add it.

Take world. Its first link is the other dot com page. Wrong host. Skip. Its second link is sports. Already seen. Skip.

The queue is empty. We return home, sports, and world.

To check it: the other dot com page was never added. And each page appears once, even though the pages link to each other in circles.

Each page is queued once, and each link is looked at once. If a pages and b links, time is O of a plus b. The seen set and the queue hold up to every page: O of a space.

So that is Web Crawler. A crawl is just a graph search, with two guards: remember where you have been, and stay on your own site.

Follow for more if you want to really understand the problems interviews ask. Code included.
```


---

## Part 44 - Exclusive Time of Functions (LeetCode 636) - 632 words, about 3:37

Reported at: Anthropic (4 problems on record, all older than six months)

```
Today, LeetCode problem six hundred thirty six. Exclusive Time of Functions.

Here is the plan. Functions call other functions, so at any moment a stack of functions is running, and the one on top is the one doing the work. Each log line says when something started or ended. The time since the previous log line belongs to whichever function was on top. Add it to that function, and move on.

There are two functions, zero and one. The log has four lines. Function zero starts at time zero. Function one starts at time two. Function one ends at time five. Function zero ends at time six. We return how much time each function ran, not counting time spent in the functions it called. That is its exclusive time.

What makes this hard is that a function's time comes in pieces. Function zero ran before it called function one, and again after. Taking its end time minus its start time, plus one, would count the whole call to function one as well. That gives seven, but function zero's true time is three.

There is one more trap. An end log at time five means the function ran through the whole of time unit five. So the end is inclusive.

The direct way steps through every single time unit, and gives it to whichever function is running. If a log ran for a billion time units, that is a billion steps for a handful of log lines. The bottleneck is stepping through time, when only the log lines matter.

Now the code. It has three parts.

First, the setup. Result is a list of zeros, one per function. Stack holds the running functions. Prev is the time of the last event, and starts at zero.

Second, the loop over the logs. Each log is split at the colons into an id, a kind, and a time. The id and time become numbers.

Third, the two kinds. For a start: if something is already running, it ran from prev up to now, so add the time minus prev to the function on top. Then push the new function, and set prev to now.

For an end: the function on top ran from prev through now, inclusive. So pop it, and add time minus prev, plus one. Then prev becomes time plus one, because the next time unit starts after this one.

We return the result.

Now run it. The first log. Function zero starts at time zero. Nothing is running yet, so nothing is added. Zero goes on the stack. Prev is zero.

Function one starts at time two. Function zero was on top, and ran from zero to two. Two units go to function zero. One goes on the stack. Prev is two.

Function one ends at time five. It ran from two through five inclusive: five minus two, plus one, is four. Pop it. Function one has four. Prev becomes six.

Function zero ends at time six. It ran from six through six: six minus six, plus one, is one. Function zero now has two plus one, which is three.

We return three and four.

To check it: the timeline has seven time units, zero to six. Three plus four is seven, and every unit belongs to exactly one function.

One pass over the logs: O of m time, for m log lines. The stack holds at most one entry per nested call, so O of n space for n functions. The direct way depended on how many time units there were.

So that is Exclusive Time of Functions. Cut the timeline at each event, and give every slice to the function on top of the stack.

Follow for more if you want to really understand the problems interviews ask. Code included.
```


---

## Part 45 - Edit Distance (LeetCode 72) - 580 words, about 3:19

Reported at: Meta, Apple, Google, Amazon, Microsoft

```
Today, LeetCode problem seventy two. Edit Distance.

Here is the plan. Fill in a table. The cell at row i and column j holds the fewest edits to turn the first i letters of the first word into the first j letters of the second word. Each cell is worked out from three neighbours that are already filled in. The bottom right cell is the answer.

The first word is horse. The second word is ros. In one edit we may insert a letter, delete a letter, or replace a letter. We return the fewest edits that turn horse into ros.

The direct way tries every edit at every step. Look at the ends of the words. If the last letters match, drop them both. If not, try a delete, an insert, and a replace, and keep the cheapest. Each choice leads to more choices, and the work grows exponentially. On this tiny pair, that is already seventy seven calls. The bottleneck is that the same pair of word beginnings is solved over and over, from different routes. The table has only twenty four cells, and each one needs solving once.

Now look at one cell. We compare the last letter of the first i letters, with the last letter of the first j letters. If they match, no edit is needed for them, so the cell equals the cell diagonally up and left. If they differ, we pay one edit, plus the cheapest of three neighbours. The cell above means we deleted a letter from the first word. The cell to the left means we inserted a letter. The cell diagonally up and left means we replaced a letter.

The edges are easy. Turning i letters into nothing costs i deletions. Turning nothing into j letters costs j insertions.

Now the code. It has three parts.

First, the table d, with one more row and one more column than the lengths, because of the empty prefix.

Second, the edges. The first column holds zero, one, two, and so on. The first row does too.

Third, two loops over the other cells. If the letters match, copy the diagonal. Otherwise, take up, left, and diagonal, and put one plus the smallest. At the end, we return the bottom right cell.

Now run it. The first row is zero, one, two, three. The first column is zero to five.

Row h. Turning h into r, o, or s costs one, two, three. All of them are mismatches.

Row o. The o matches the o of ros, so that cell copies its diagonal, which is one. Turning ho into ro costs one edit: replace h with r.

Skip ahead to the last cell. Row e, column s. The letters e and s differ. Up is two. Left is four. Diagonal is three. The smallest is two. Add one: three.

We return three.

To check it: horse becomes rorse by replacing h with r. Rorse becomes rose by deleting an r. Rose becomes ros by deleting the e. Three edits.

The table has m times n cells, and each costs a few steps: O of m times n time, and O of m times n space. The direct way was exponential.

So that is Edit Distance. A big question about two words becomes a table of small questions about their beginnings, and each answer comes from three neighbours.

Follow for more if you want to really understand the problems interviews ask. Code included.
```


---

## Part 46 - Median of Two Sorted Arrays (LeetCode 4) - 826 words, about 4:43

Reported at: Meta, Apple, Google, Amazon, Microsoft

```
Today, LeetCode problem four. Median of Two Sorted Arrays.

Here is the plan. The median splits all the numbers into a left half and a right half of equal size, where everything on the left is at most everything on the right. We do not need to merge the arrays to find that split. We only need to decide how many numbers the left half takes from the first array. The rest come from the second. A binary search finds that number.

The first array is two, seven, eleven, fourteen. The second is one, four, five, ten. Both are sorted. Together they hold eight numbers. We return their median. With eight numbers, that is the average of the fourth and the fifth.

The direct way merges the two arrays into one sorted list, and picks the middle. That takes O of m plus n, because every number is looked at. The bottleneck is that we sort out all eight numbers, when we only need the two in the middle. The problem asks for something much faster, O of log of the smaller array.

So think about the split. The left half holds four numbers. Say it takes i from the first array. Then it must take four minus i from the second. There are only a few possible values of i, zero to four, and we can binary search among them.

How do we know if a split is right? Look at the four numbers on the borders. A left is the last number the first array gives to the left half. A right is the first number it keeps for the right half. The second array has the same pair. Each array is sorted, so its own left is at most its own right. The split is right when each left is at most the other array's right. If the first array's left is bigger than the second's right, the first array gave too many, so move i down. If the second array's left is bigger than the first's right, the first gave too few, so move i up.

When an array gives nothing, its left is minus infinity. When it gives everything, its right is plus infinity.

Now the code. It has three parts.

First, make sure a is the shorter array, by swapping if not. Then m and n are the lengths. Half is the size of the left half: m plus n plus one, divided by two. When the total is odd, the left half gets the extra number.

Second, the search. Lo is zero, and hi is m. While lo is not past hi, i is the middle. J is half minus i. Then the four borders, using infinity when an array is empty on that side.

Third, the three cases. If a left is bigger than b right, hi moves to i minus one. Else if b left is bigger than a right, lo moves to i plus one. Otherwise the split is right. Low is the larger of the two lefts. If the total is odd, return low. If even, high is the smaller of the two rights, and we return their average.

Now run it. Lo is zero, hi is four. I is two, and j is two. The first array gives two and seven, and keeps eleven and fourteen. The second gives one and four, and keeps five and ten. Seven, the first left, is bigger than five, the second right. Too many from the first array. Hi moves to one.

Lo is zero, hi is one. I is zero, and j is four. The first array gives nothing, so its left is minus infinity, and its right is two. The second gives all four, so its left is ten, and its right is plus infinity. Ten is bigger than two. Too few from the first array. Lo moves to one.

Lo is one, hi is one. I is one, and j is three. The first array gives two, and keeps seven. The second gives one, four, and five, and keeps ten. Two is at most ten. Five is at most seven. The split is right.

The left half is one, two, four, and five. Low is five. The total is even, so high is the smaller of seven and ten, which is seven. We return five plus seven, divided by two. Six.

To check it: merged, the numbers are one, two, four, five, seven, ten, eleven, fourteen. The middle two are five and seven. Their average is six.

Each step halves the range of the shorter array: O of log of the smaller length. A few variables: O of one space. Merging was O of m plus n.

So that is Median of Two Sorted Arrays. Do not merge. Search for the split that puts the right numbers on each side.

Follow for more if you want to really understand the problems interviews ask. Code included.
```
