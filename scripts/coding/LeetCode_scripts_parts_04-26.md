# LeetCode, Line by Line - scripts for Parts 04 to 26

Paste the block under each part into the voice model. Every solution, example and figure was checked by running code against a brute force.

| Part | Problem | Approach | Length |
|---|---|---|---|
| 04 | 3. Longest Substring Without Repeating Characters | Sliding window with a set (the version interviewers expect first | ~2:57 |
| 05 | 20. Valid Parentheses | Stack of open brackets | ~2:42 |
| 06 | 121. Best Time to Buy and Sell Stock | Running minimum, one pass | ~2:29 |
| 07 | 704. Binary Search | Iterative binary search with inclusive bounds (lo <= hi) | ~2:41 |
| 08 | 206. Reverse Linked List | Iterative, in place, three pointers (prev, curr, nxt) | ~2:34 |
| 09 | 15. 3Sum | Sort, fix one number, two pointers for the other two, skip duplicates | ~2:59 |
| 10 | 11. Container With Most Water | Two pointers from both ends, always moving the shorter wall | ~2:41 |
| 11 | 49. Group Anagrams | Hash map keyed by the sorted letters of each word | ~2:39 |
| 12 | 238. Product of Array Except Self | Prefix products into the answer array, then a running suffix product. No division | ~2:40 |
| 13 | 128. Longest Consecutive Sequence | Hash set | ~2:39 |
| 14 | 104. Maximum Depth of Binary Tree | Recursive DFS: 1 + max(depth(left), depth(right)) | ~2:22 |
| 15 | 102. Binary Tree Level Order Traversal | BFS with a deque | ~2:38 |
| 16 | 98. Validate Binary Search Tree | Recursion with (low, high) bounds passed down | ~2:47 |
| 17 | 70. Climbing Stairs | Bottom-up DP with two variables | ~2:12 |
| 18 | 198. House Robber | DP with two variables: take (prev + money) or skip (curr) | ~2:25 |
| 19 | 322. Coin Change | Bottom-up DP table over amounts 0..amount | ~2:52 |
| 20 | 56. Merge Intervals | Sort by start, then one sweep extending the last merged interval | ~2:36 |
| 21 | 994. Rotting Oranges | Multi-source BFS, one queue level per minute | ~3:07 |
| 22 | 207. Course Schedule | Topological sort with in-degree counts (Kahn's algorithm) | ~2:39 |
| 23 | 347. Top K Frequent Elements | Counter + bucket sort by frequency (O(n)) | ~2:31 |
| 24 | 76. Minimum Window Substring | Sliding window with a need counter and a missing count | ~3:11 |
| 25 | 146. LRU Cache (1 of 2): the design | Hash map + doubly linked list, using Python's OrderedDict | ~2:51 |
| 26 | 146. LRU Cache (2 of 2): built by hand | Doubly linked list with sentinel head and tail + dict of key -> node | ~2:57 |

## Part 04 - Longest Substring Without Repeating Characters (LeetCode 3)

Example: "abcbad" -> 4 ("cbad")

```
Today, LeetCode problem three. Longest Substring Without Repeating Characters.

Here is the plan. Keep a window of characters with no repeats. Grow it on the right, one character at a time. When a repeat walks in, shrink it from the left until the repeat is gone. The longest window we ever hold is the answer.

The string is a, b, c, b, a, d. Six characters. We want the length of the longest stretch where no character appears twice.

The direct way tries every starting point, and from each one extends to the right until a character repeats. On this string, that is seventeen character checks. The waste is in the restart. After a repeat, it starts again from the next position, and checks characters it already knows are unique. For a long string, that is O of n squared.

Now notice what a repeat really tells us. If the window is a, b, c, and another b arrives, the only problem is the old b. Everything after it is still fine. So we do not restart. We move the left edge just past the old b, and keep the rest.

That moving range is called a sliding window. To know instantly whether a character is inside it, we keep its characters in a set.

Now the code. It has three parts.

First, the setup. An empty set called seen, a left edge at zero, and the best length so far, zero.

Second, the main loop. The right edge walks over every character. While the new character is already in the set, we remove the character at the left edge, and move left forward by one.

Third, once the repeat is gone, we add the new character to the set, and update best with the window's length: right minus left, plus one.

Now run it. A goes in. The window is a, length one. B goes in. Length two. C goes in. Length three. Best is three.

Then b arrives, and b is already in the set. We remove a, the leftmost character. B is still in the set, so we remove b too. Now the window is just c, and the new b can join. The window is c, b. Length two.

Next, a. It left the set earlier, so it joins freely. C, b, a. Length three.

Then d. C, b, a, d. Length four. Best becomes four.

The loop ends. We return four.

To check it: c, b, a, d has no repeats. Adding the b before it would repeat b, and nothing comes after it. Four.

Each character enters the set once, and leaves it at most once. So the time is O of n. The set never holds more than the window, so the extra space is O of n at most. The direct way was O of n squared.

So that is the sliding window. Grow on the right, shrink on the left only as far as the repeat forces you, and never restart.

Follow for more if you want to really understand the problems interviews ask. Code included.
```

## Part 05 - Valid Parentheses (LeetCode 20)

Example: "([]{})" -> true

```
Today, LeetCode problem twenty. Valid Parentheses.

Here is the plan. Walk through the string once. Every opening bracket waits on a stack. Every closing bracket must match the bracket on top of the stack, the one opened most recently. If it does, both are done. If anything fails to match, or something is left waiting at the end, the string is invalid.

Our string is: open round, open square, close square, open curly, close curly, close round. Six characters. It is valid when every opener is closed by the same type, in the right order.

The direct way deletes every adjacent pair, like an open and close round, again and again, until nothing changes. If the string ends up empty, it was valid. Here, two passes delete pairs, and a third finds nothing left to delete. The bottleneck is the rescanning. Each pass reads the whole string again, to find pairs that only appeared because of the last deletion. In the worst case, that is O of n squared.

Notice which pair always disappears first. It is a closer right after its opener. So the bracket a closer must match is always the latest opener that is still unclosed. Last in, first out. That structure is called a stack.

Now the code. It has three parts.

First, a map from each closing bracket to its opening partner, and an empty stack.

Second, the loop over every character. An opener is pushed on the stack. A closer checks the top. If the stack is empty, or the top is not its partner, we return false right away. Otherwise, we pop the top.

Third, after the loop, we return true only if the stack is empty, so no opener is left waiting.

Now run it. Open round. Pushed. The stack holds round.

Open square. Pushed. The stack holds round, square.

Close square. Its partner is open square, and that is on top. Pop. The stack holds round again.

Open curly is pushed, and close curly pops it, the same way.

Close round. Its partner is open round, and it is on top. Pop. The stack is empty.

The loop ends with an empty stack. We return true.

To check the failure cases: open round, then close square, fails at once, because the top is round, not square. And two open rounds with nothing else fail at the end, because the stack still holds them.

Each character is pushed or popped once. O of n time. The stack can hold up to n openers, so O of n space. The direct way was O of n squared.

So that is Valid Parentheses. A closer must always match the most recent unclosed opener, and a stack keeps exactly that bracket on top.

Follow for more if you want to really understand the problems interviews ask. Code included.
```

## Part 06 - Best Time to Buy and Sell Stock (LeetCode 121)

Example: [7, 2, 5, 1, 6, 4] -> 5 (buy at 1, sell at 6)

```
Today, LeetCode problem one hundred twenty one. Best Time to Buy and Sell Stock.

Here is the plan. Walk through the days once. Remember the cheapest price seen so far. On each day, ask what we would earn if we sold today, having bought at that cheapest price. The best of those answers is the result.

The prices over six days are seven, two, five, one, six, four. We may buy once and sell once, and the sale must come after the purchase. We want the biggest profit, or zero if there is none.

The obvious shortcut fails. The highest price is seven and the lowest is one, a difference of six. But seven comes before one, so we cannot buy at one and sell at seven. Order matters.

The direct way tries every pair of buy day and sell day. Six days give fifteen pairs. For each sell day, it searches all the earlier days for the cheapest one. That search is the bottleneck: it repeats work the previous day already did. O of n squared.

Notice that the cheapest earlier price can be carried forward. When we move to the next day, the cheapest price so far is either the old cheapest, or today's price. One comparison updates it. That carried value is called a running minimum.

Now the code. It has two parts.

First, the setup. Lowest starts at the first price, and best starts at zero.

Second, the loop over every price. Lowest becomes the smaller of lowest and today's price. Then best becomes the larger of best, and today's price minus lowest. That difference is today's profit, if we sell.

Now run it. Day one, price seven. Lowest is seven. Profit zero.

Day two, price two. Lowest drops to two. Profit zero.

Day three, price five. Five minus two is three. Best is three.

Day four, price one. Lowest drops to one. Profit zero. Best stays three.

Day five, price six. Six minus one is five. Best becomes five.

Day six, price four. Four minus one is three. Best stays five.

We return five.

To check it: buy on day four at one, and sell on day five at six. Six minus one is five, and the purchase comes first.

One pass over the prices: O of n time. Only two numbers are stored: O of one space. The direct way was O of n squared.

So that is the running minimum. Carry the cheapest price forward, and every day becomes a single subtraction.

Follow for more if you want to really understand the problems interviews ask. Code included.
```

## Part 07 - Binary Search (LeetCode 704)

Example: [1, 3, 5, 7, 9, 11, 13], target 9 -> 4

```
Today, LeetCode problem seven hundred four. Binary Search.

Here is the plan. The array is sorted, so one look at the middle tells us which half cannot hold the target. We throw that half away, and look at the middle of what is left. Each look halves the search.

The array is one, three, five, seven, nine, eleven, thirteen. Seven numbers, sorted. The target is nine. We return its index, or minus one if it is not there.

The direct way checks the numbers one by one from the left. Nine is found on the fifth check. For n numbers, that is up to n checks: O of n. The bottleneck is that each check rules out only one number, even though the array is sorted.

Now use the order. If the middle number is smaller than the target, every number to its left is smaller too. So one comparison rules out half the array. Repeating this is called binary search.

Now the code. It has two parts.

First, two edges. Lo starts at index zero, and hi at the last index. If the target is present, it is always between them.

Second, the loop, which runs while lo is not past hi. Mid is the middle index. If the number there is the target, we return mid. If it is smaller than the target, the answer is to the right, so lo moves to mid plus one. Otherwise, hi moves to mid minus one. If the loop ends, the edges have crossed, and we return minus one.

Now run it. Lo is zero, hi is six. Mid is three, and the number there is seven. Seven is smaller than nine, so lo moves to four. The left half is gone.

Now lo is four, and hi is six. Mid is five, and the number is eleven. Eleven is bigger than nine, so hi moves to four.

Lo and hi are both four. Mid is four, and the number is nine. Found. We return four.

Three checks instead of five.

To check it: index four holds nine. And if the target were eight, the same three steps would end with lo at four and hi at three. The edges cross, so we return minus one.

That is why the loop runs while lo is less than or equal to hi. When they are equal, one number is still left to check.

Each check halves the range: O of log n time. A million numbers need at most twenty checks. Only a few indexes are stored: O of one space. The direct way was O of n.

So that is binary search. In a sorted array, one comparison at the middle removes half of what is left.

Follow for more if you want to really understand the problems interviews ask. Code included.
```

## Part 08 - Reverse Linked List (LeetCode 206)

Example: 1 -> 2 -> 3 -> 4 becomes 4 -> 3 -> 2 -> 1

```
Today, LeetCode problem two hundred six. Reverse Linked List.

Here is the plan. Walk down the list once, and turn each arrow around, so it points backwards. Before turning an arrow, save where it pointed, or the rest of the list is lost. When the walk ends, the last node is the new head.

The list is one, then two, then three, then four. Each node holds a value, and an arrow to the next node. We want four, three, two, one, and we return the new head.

The direct way copies the four values into an array, then walks the list again and writes them back in reverse. It works, and it is O of n time. The cost is memory: an extra array as long as the list. Interviewers want it done in place.

Doing it in place has one danger. A node's arrow is the only way to reach the rest of the list. Turn it around first, and everything after it is gone. So we always save the next node before changing the arrow.

That needs three pointers. Prev is the part already reversed. Curr is the node we are turning. And next is the saved rest of the list.

Now the code. It has two parts.

First, the setup. Prev starts as none, because the old head will become the tail, pointing to nothing. Curr starts at the head.

Second, the loop, which runs while curr exists. Four steps, always in this order. Save curr's next, in a variable called nxt. Point curr's arrow back at prev. Move prev forward to curr. Move curr forward to the saved next. When curr runs off the end, prev is the new head, and we return it.

Now run it. Curr is one. Save two. One now points to none. Prev moves to one, and curr to two.

Curr is two. Save three. Two now points back to one. Prev is two, and curr is three.

Three and four go the same way. Three points to two. Four points to three.

Curr becomes none, and the loop ends. Prev is four. We return four.

To check it: from four, the arrows go to three, two, one, and then none. Every node was visited once, and no node was lost.

Each node is visited once: O of n time. Only three pointers are stored: O of one extra space. The direct way also took O of n time, but O of n extra memory.

So that is reversing a list in place. Save the next node, turn the arrow, then step forward.

Follow for more if you want to really understand the problems interviews ask. Code included.
```

## Part 09 - 3Sum (LeetCode 15)

Example: [-1, 0, 1, 2, -1, -4] -> [[-1, -1, 2], [-1, 0, 1]]

```
Today, LeetCode problem fifteen. Three Sum.

Here is the plan. Sort the numbers. Fix one number at a time, and look for two more that cancel it out. Because the array is sorted, two pointers find that pair in one sweep. Skipping repeated values keeps every answer unique.

The numbers are minus one, zero, one, two, minus one, minus four. We want every group of three that adds up to zero, with no group repeated.

The direct way tries every group of three. Six numbers give twenty groups. A thousand numbers give over a hundred and sixty six million. That is O of n cubed, and it still needs extra work to remove repeated groups. The bottleneck is the innermost search: for each pair, it scans for the third number.

Once we fix the first number, the problem becomes: find two numbers that add up to its opposite. In a sorted array, that is a two pointer search. If the sum is too small, move the left pointer right. If it is too big, move the right pointer left.

Sorted, the numbers are minus four, minus one, minus one, zero, one, two.

Now the code. It has three parts.

First, sort, and prepare the result list.

Second, the outer loop picks index i as the fixed number. If it equals the number before it, we skip it, since it would find the same groups again. Then j starts just after i, and k at the end.

Third, the inner loop runs while j is before k. If the total is below zero, j moves right. If it is above zero, k moves left. If it is exactly zero, we record the group, move j right, and keep moving it while it lands on the same value as before.

Now run it. Fix minus four. Even its two biggest partners, one and two, only reach minus one. Every total stays below zero, so j walks until it meets k. No group.

Fix minus one. J is the other minus one, and k is two. Minus one, minus one, two: zero. Recorded. J moves to zero.

Now minus one, zero, two is one. Too big, so k moves to one. Minus one, zero, one: zero. Recorded.

The next i is minus one again. It repeats the value before it, so it is skipped.

Fix zero. Zero, one, two is three. Too big. K moves left, and the pointers meet.

We return two groups: minus one, minus one, two. And minus one, zero, one.

To check it: both groups add up to zero, and among all twenty groups of three, these are the only two distinct ones that do.

Sorting is O of n log n. Then, for each fixed number, one sweep of the pointers: O of n squared in total. Extra space is just the pointers, plus whatever the sort uses. The direct way was O of n cubed.

So that is Three Sum. Sort, fix one number, and turn the rest into a two pointer search, skipping repeats.

Follow for more if you want to really understand the problems interviews ask. Code included.
```

## Part 10 - Container With Most Water (LeetCode 11)

Example: [4, 6, 8, 3, 7, 1] -> 18 (walls 6 and 7, three apart)

```
Today, LeetCode problem eleven. Container With Most Water.

Here is the plan. Start with the widest container, a wall at each end. Then move the shorter wall inward, one step at a time, and keep the best area seen. Moving the shorter wall is safe, because that wall has already had its best container.

There are six walls, with heights four, six, eight, three, seven, one. Any two walls, with the floor between them, hold water. The amount is the distance between them, times the shorter wall. We want the most water.

The direct way tries every pair of walls. Six walls give fifteen pairs: O of n squared. The bottleneck is that it never learns anything from a pair. A short wall it has already measured is measured again with every other partner.

Now look at one container. Its water is capped by the shorter wall. Keep that short wall, and move the other wall inward. The container gets narrower, and it is still capped by the same short wall, or by something lower. It can never hold more. So once a short wall has been paired with the farthest wall on the other side, it is finished. We can drop it.

Now the code. It has two parts.

First, the setup. Left at the first wall, right at the last, and best at zero.

Second, the loop, while left is before right. H is the shorter of the two walls. The area is h times the distance between them, and best keeps the larger. Then whichever wall is shorter moves inward. If they are equal, we move the right one.

Now run it. Left is four, right is one. The distance is five, and the shorter wall is one. Area five. The right wall is shorter, so it moves in.

Left is four, right is seven, distance four. Area sixteen. Now the left wall is shorter. It moves in.

Six and seven, distance three. Area eighteen. Best is eighteen. The left is shorter again, so it moves to eight.

Eight and seven, distance two. Area fourteen. Now the right is shorter. It moves to three.

Eight and three, distance one. Area three. The right moves again, and the pointers meet.

We return eighteen.

To check it: the walls six and seven stand three apart. Three times six is eighteen, and none of the fifteen pairs does better.

Each step drops one wall: O of n time. Only two pointers and the best area: O of one space. The direct way was O of n squared.

So that is Container With Most Water. The shorter wall caps every container it is in, so once it has had its widest chance, it can go.

Follow for more if you want to really understand the problems interviews ask. Code included.
```

## Part 11 - Group Anagrams (LeetCode 49)

Example: ["eat","tea","tan","ate","nat","bat"] -> [["eat","tea","ate"],["tan","nat"],["bat"]]

```
Today, LeetCode problem forty nine. Group Anagrams.

Here is the plan. Give every word a signature that is the same for all of its anagrams: its letters in sorted order. Then put each word in a hash map, under its signature. Each bucket of the map is one group.

The words are eat, tea, tan, ate, nat, bat. Two words are anagrams when they use exactly the same letters, the same number of times. We want the words grouped that way.

The direct way compares words in pairs. Six words make fifteen pairs, and each comparison has to sort or count both words. For n words, that is O of n squared comparisons. The bottleneck is the pairing: every word is checked against every other word.

Now ask what anagrams have in common. Sort the letters of eat, and you get a, e, t. Sort tea, and you get a, e, t too. Sorting turns every anagram into the same string. That string is called a canonical key. Two words share a key exactly when they are anagrams. So we never compare words with each other. Each word is only turned into its own key.

Now the code. It has two parts.

First, a dictionary called groups, where a missing key starts as an empty list.

Second, the loop over the words. For each word, the key is its letters, sorted and joined back into a string. The word is appended to the list under that key. At the end, we return all the lists.

Now run it. Eat sorts to a, e, t. A new key, so a new group: eat.

Tea also sorts to a, e, t. It joins eat.

Tan sorts to a, n, t. A new group.

Ate sorts to a, e, t, and joins eat and tea. Nat sorts to a, n, t, and joins tan.

Bat sorts to a, b, t. A group of its own.

We return three groups. Eat, tea, ate. Tan, nat. And bat.

To check it: each group shares its letters exactly, and no two groups do.

Each of the n words is sorted once. If a word has k letters, that is O of n times k log k time. The map stores every word once: O of n times k space. The direct way needed O of n squared comparisons.

If an interviewer asks for better, count the letters instead of sorting them. For lowercase words, a count of twenty six numbers is also a key, and building it is O of k.

So that is Group Anagrams. Turn each word into a key all its anagrams share, and let a hash map do the grouping.

Follow for more if you want to really understand the problems interviews ask. Code included.
```

## Part 12 - Product of Array Except Self (LeetCode 238)

Example: [2, 3, 4, 5] -> [60, 40, 30, 24]

```
Today, LeetCode problem two hundred thirty eight. Product of Array Except Self.

Here is the plan. The product of everything except one number is two parts multiplied together: everything to its left, and everything to its right. One pass from the left builds the left parts. One pass from the right multiplies in the right parts. No division needed.

The numbers are two, three, four, five. For each position, we want the product of all the other numbers. The problem forbids division, and asks for O of n time.

Dividing the total product by each number would be the obvious trick, and it is not allowed. It would also break when a number is zero.

The direct way multiplies the other numbers for each position. Four positions, each multiplying three numbers. For n numbers, that is O of n squared. The bottleneck: neighbouring positions recompute almost the same product. The left side of position two is the left side of position one, times one more number.

So we carry the products forward. The product of everything before a position is called a prefix product. The product of everything after it is a suffix product. Each one grows with a single multiplication per step.

Now the code. It has three parts.

First, an answer array, filled with ones.

Second, the left pass. Prefix starts at one. At each index, the answer takes the current prefix, and then prefix is multiplied by that index's number. So each answer holds the product of everything to its left.

Third, the right pass, from the last index down. Suffix starts at one. Each answer is multiplied by the current suffix, and then suffix is multiplied by that index's number. Now each answer also includes everything to its right.

Now run the left pass. Index zero gets one, since nothing is to its left. Index one gets two. Index two gets two times three, six. Index three gets six times four, twenty four.

Now the right pass. Index three is multiplied by one, since nothing is to its right. It stays twenty four. Suffix becomes five.

Index two: six times five, thirty. Suffix becomes twenty.

Index one: two times twenty, forty. Suffix becomes sixty.

Index zero: one times sixty, sixty.

We return sixty, forty, thirty, twenty four.

To check it: for index zero, three times four times five is sixty. For index three, two times three times four is twenty four.

Two passes: O of n time. Apart from the answer array, only two numbers: O of one extra space. The direct way was O of n squared.

So that is Product of Array Except Self. Everything except you is everything before you, times everything after you.

Follow for more if you want to really understand the problems interviews ask. Code included.
```

## Part 13 - Longest Consecutive Sequence (LeetCode 128)

Example: [100, 4, 200, 1, 3, 2] -> 4 (1, 2, 3, 4)

```
Today, LeetCode problem one hundred twenty eight. Longest Consecutive Sequence.

Here is the plan. Put every number in a set. A run of consecutive numbers can only be counted from its first number, the one with nothing just below it. So we count runs only from those starting numbers, and every number is counted once.

The numbers are one hundred, four, two hundred, one, three, two. We want the length of the longest run of consecutive values, in any order. The problem asks for O of n time.

Sorting would line the runs up, but sorting is O of n log n.

The direct way starts from every number, and counts upward while the next value exists. Starting from one, it counts one, two, three, four. Starting from two, it counts two, three, four again. The bottleneck is recounting the same run from its middle. With one long run of n numbers, that is O of n squared.

So the question is: which number should start the count? Only the one whose value minus one is not present. That number is the start of its run. Every other number is in the middle of someone else's run, and gets skipped.

Now the code. It has two parts.

First, the setup. A set of the numbers, for instant lookups, and best at zero.

Second, the loop over the set. If x minus one is not in the set, x starts a run. We count upward while x plus length is in the set, and best keeps the longest length. If x minus one is present, we do nothing.

Now run it. The set gives us one, two, three, one hundred, four, two hundred, in that order.

One. Zero is not in the set, so one starts a run. Two is there, three is there, four is there, and five is not. Length four. Best is four.

Two. One is in the set, so two is in the middle of a run. Skipped. Three is skipped the same way.

One hundred. Ninety nine is not there, so it starts a run. But one hundred one is missing. Length one.

Four is skipped, because three is there. Two hundred starts a run of length one.

We return four.

To check it: one, two, three, four are all present, and neither zero nor five is.

Each number starts at most one count, and is counted only inside the run it belongs to. O of n time. The set holds every number: O of n space. The direct way was O of n squared.

So that is Longest Consecutive Sequence. Only count from the start of a run, and every run is counted exactly once.

Follow for more if you want to really understand the problems interviews ask. Code included.
```

## Part 14 - Maximum Depth of Binary Tree (LeetCode 104)

Example: [3, 9, 20, null, null, 15, 7] -> 3

```
Today, LeetCode problem one hundred four. Maximum Depth of Binary Tree.

Here is the plan. The depth of a tree is one, for the root, plus the depth of its deeper subtree. Each subtree is a smaller tree, so we answer it the same way. An empty tree has depth zero, and that is where the recursion stops.

Our tree has root three. Its left child is nine, a leaf. Its right child is twenty, which has two children, fifteen and seven. Depth is the number of nodes on the longest path from the root down to a leaf.

What makes this hard is that the root cannot see the bottom. The longest path could go anywhere. Listing every root to leaf path, and measuring each one, works, but it stores paths we do not need.

Instead, let every node answer one question for its parent: how deep am I? A leaf answers one. Any other node answers one, plus the larger of its children's answers. The answers flow upward, and the root's answer is the depth. This is called recursion, and here it works in post order: children first, then the parent.

Now the code. It has two parts.

First, the stopping case. If the node is empty, return zero.

Second, the recursive case. Ask the left subtree for its depth, then the right subtree. Return one plus the larger of the two.

Now run it. We start at three, which first asks nine. Nine's children are empty, so they return zero. Nine returns one plus zero: one.

Then three asks twenty. Twenty asks fifteen, which returns one. Twenty asks seven, which returns one. Twenty returns one plus one: two.

Back at three. The left side said one, and the right side said two. Three returns one plus two: three.

The depth is three.

To check it: the path three, twenty, fifteen has three nodes, and no path is longer.

Every node is visited once: O of n time. The recursion keeps one call per level of the current path, so the space is O of the tree's height. That is O of log n for a balanced tree, and O of n if the tree is a single line. Listing every path would also store them; this stores only the calls.

So that is Maximum Depth. Each node asks its children how deep they are, and adds one.

Follow for more if you want to really understand the problems interviews ask. Code included.
```

## Part 15 - Binary Tree Level Order Traversal (LeetCode 102)

Example: [1, 2, 3, 4, null, 5, 6] -> [[1], [2, 3], [4, 5, 6]]

```
Today, LeetCode problem one hundred two. Binary Tree Level Order Traversal.

Here is the plan. Visit the tree level by level, with a queue. The trick is knowing where one level ends. Before we start a level, the queue holds exactly that level's nodes, so we count them, and take exactly that many.

The tree has root one. One's children are two and three. Two has a left child, four. Three has two children, five and six. We want the values grouped by level: one, then two and three, then four, five, six.

A queue visits nodes in the right order, top to bottom and left to right. What makes this hard is the grouping. A plain queue is one long line. By the time we take three, two's child four is already queued behind it, and nothing marks where level two stops.

The fix is a snapshot. When a new level starts, the queue holds that level, and nothing else. Its length is the level's size. We remove exactly that many nodes, and the children they add wait for the next round. Visiting a tree this way is called breadth first search.

Now the code. It has three parts.

First, an empty tree returns an empty list. Otherwise, the queue starts with the root.

Second, the outer loop runs while the queue has nodes. Each round starts an empty level list, and reads the queue's length once.

Third, the inner loop runs exactly that many times. It removes a node from the front, adds its value to the level, and adds its left and right children to the back. When the inner loop ends, the level goes into the result.

Now run it. The queue holds one. Length one. We take one, and add two and three. The first level is done: one.

The queue holds two and three. Length two. We take two, and add four. We take three, and add five and six. The queue now has three nodes, but we took only two. The second level: two, three.

The queue holds four, five, six. Length three. None of them has children. The third level: four, five, six.

The queue is empty. We return the three levels.

To check it: one is at the top, two and three are its children, and four, five, six are the children of the second level.

Each node enters and leaves the queue once: O of n time. The queue holds at most one level, which can be about half the nodes: O of n space.

So that is Level Order Traversal. Before each level, the queue's length tells you exactly how many nodes belong to it.

Follow for more if you want to really understand the problems interviews ask. Code included.
```

## Part 16 - Validate Binary Search Tree (LeetCode 98)

Example: root 5; 5.left 3, 5.right 8; 3.left 2, 3.right 6 -> false (6 is in 5's left subtree)

```
Checking that every node is bigger than its left child, and smaller than its right child, sounds like enough to validate a binary search tree. It is not. Today, LeetCode problem ninety eight. Validate Binary Search Tree.

Here is the plan. Every node carries a range it must fall inside. The root may be anything. Going left, the parent's value becomes the upper limit. Going right, it becomes the lower limit. One node outside its range makes the whole tree invalid.

Our tree has root five. Its left child is three, and its right child is eight. Three has two children: two on the left, and six on the right. In a valid tree, everything in a node's left subtree is smaller than it, and everything in its right subtree is bigger.

Now check each parent with its children. Five has three on the left and eight on the right: fine. Three has two on the left and six on the right: fine. Every local check passes. But six sits in five's left subtree, and six is bigger than five. The tree is invalid. The local check never compares six with five.

So a node must respect every ancestor above it, not only its parent. We do not need to remember all of them. Only two numbers matter: the tightest lower limit, and the tightest upper limit. That pair is called the node's bounds.

Now the code. It has two parts.

First, a helper called check, which takes a node and its bounds, low and high. An empty node is valid. If the node's value is not strictly between low and high, it returns false. Otherwise, it checks the left child with the upper bound tightened to this value, and the right child with the lower bound raised to this value. Both must pass.

Second, the main function calls check on the root, with minus infinity and plus infinity as the bounds.

Now run it. Five, with no limits. Fine. Its left child, three, must be below five. Fine.

Two, on the left of three, must be below three. Fine. Its children are empty.

Six, on the right of three, must be above three and below five. The upper limit five came from the root. Six is not below five, so it returns false.

That false travels up through three, and through five. The right subtree, eight, is never even checked. We return false.

To check it: six is in the left subtree of five, so it must be smaller than five, and it is not.

Each node is checked once: O of n time. The recursion uses one call per level: O of the tree's height in space.

So that is Validate Binary Search Tree. A node answers to all of its ancestors, and two bounds carry everything they require.

Follow for more if you want to really understand the problems interviews ask. Code included.
```

## Part 17 - Climbing Stairs (LeetCode 70)

Example: n = 5 -> 8

```
Today, LeetCode problem seventy. Climbing Stairs.

Here is the plan. To stand on any step, your last move was either one step or two. So the ways to reach a step are the ways to reach the step below, plus the ways to reach the one below that. We build that up from the bottom, keeping just two numbers.

There are five steps. Each move climbs one step, or two. We want the number of different ways to reach the top.

The direct way is a recursive function: ways of n is ways of n minus one, plus ways of n minus two. It is correct, and painfully slow. For five steps, it makes fifteen calls. For thirty steps, it makes about two point seven million. The bottleneck is repetition. Inside ways of five, ways of three is computed twice, and the smaller steps even more often. The calls grow exponentially.

But each step's answer never changes. So compute it once, from the bottom up, and reuse it. Saving the answers to smaller subproblems is called dynamic programming. And since each step only needs the two answers below it, we keep only two numbers.

Now the code. It has two parts.

First, two variables, prev and curr. They both start at one. There is one way to stand at the ground, and one way to reach step one.

Second, a loop from step two up to n. Each round, the new curr is prev plus curr, and prev takes the old curr. After the loop, curr is the answer for step n.

Now run it. Step two: one plus one, two ways. Step three: one plus two, three ways. Step four: two plus three, five. Step five: three plus five, eight.

We return eight.

To check it, list the ways to reach step three. One, one, one. One, two. And two, one. Three ways, as the loop said.

One loop up to n: O of n time. Two variables: O of one space. The direct recursion was exponential.

These numbers are the Fibonacci sequence, shifted by one.

So that is Climbing Stairs. Every answer is built from the two answers just below it, and each one is computed only once.

Follow for more if you want to really understand the problems interviews ask. Code included.
```

## Part 18 - House Robber (LeetCode 198)

Example: [2, 1, 1, 9] -> 11 (houses 1 and 4)

```
Today, LeetCode problem one hundred ninety eight. House Robber.

Here is the plan. Walk past the houses one by one. At each house there are only two choices. Rob it, and add it to the best total from two houses back. Or skip it, and keep the best total from the house before. Take the bigger one. Two running numbers are all we need.

The houses hold two, one, one, and nine. You cannot rob two houses that are next to each other. We want the most money.

The tempting shortcut is to rob every other house. Houses one and three give two plus one, three. Houses two and four give one plus nine, ten. Both are wrong. The best plan is two plus nine, eleven, which skips two houses in a row.

The direct way tries every plan with no neighbours. Four houses allow eight such plans, counting robbing nothing. Twenty houses allow over seventeen thousand. The number of plans grows exponentially. The bottleneck is that plans with the same beginning work out the same partial totals again and again.

But the best total up to any house depends on only two earlier facts: the best total up to the house before, and the best total up to two houses before. That is dynamic programming again.

Now the code. It has two parts.

First, prev and curr both start at zero. Curr is the best total so far. Prev is the best total one house earlier.

Second, the loop over the houses. Taking this house gives prev plus its money. Skipping it gives curr. Curr becomes the larger, and prev takes the old curr.

Now run it. House one holds two. Take it: zero plus two, two. Skip it: zero. Best is two.

House two holds one. Take it: zero plus one, one. Skip it: two. Best stays two.

House three holds one. Take it: two plus one, three. Skip it: two. Best is three.

House four holds nine. Take it: two plus nine, eleven. Skip it: three. Best is eleven.

We return eleven.

To check it: rob the first house and the last. Two plus nine is eleven, and they are not neighbours.

One pass: O of n time. Two numbers: O of one space. The direct way was exponential.

So that is House Robber. At each house, the best is either this house plus the best from two back, or the best so far.

Follow for more if you want to really understand the problems interviews ask. Code included.
```

## Part 19 - Coin Change (LeetCode 322)

Example: coins [1, 3, 4], amount 6 -> 2 (3 + 3); greedy gives 3 (4 + 1 + 1)

```
Using the biggest coin first feels like the fastest way to make change. With coins one, three, and four, it fails. Today, LeetCode problem three hundred twenty two. Coin Change.

Here is the plan. Work out the fewest coins for every amount, from one up to the target. For each amount, try every coin as the last coin used: that coin, plus the best answer for what is left, which we already know. Keep the smallest.

The coins are one, three, and four, and we can use each as often as we like. The amount is six. We want the fewest coins that make it, or minus one if it cannot be made.

Greedy takes four first, leaving two, then one, and one. Three coins. But three plus three is also six, with only two coins. Taking the biggest coin first is not always best.

The direct way tries every combination of coins that adds up to six. For larger amounts, the combinations explode. The bottleneck is that many combinations share the same remainder, and the best answer for that remainder is worked out again every time.

Any best answer for six ends with some coin. If that last coin is three, the rest must be the best answer for three. So the answer for six is built from answers for smaller amounts. Storing those answers in a table is dynamic programming.

Now the code. It has three parts.

First, a table called dp, with one entry per amount. Dp of zero is zero coins. Every other entry starts at infinity, meaning not reachable yet.

Second, two loops. For every amount from one up to the target, and for every coin no bigger than that amount, dp of the amount becomes the smaller of its current value, and dp of the amount minus the coin, plus one.

Third, if the target's entry is still infinity, we return minus one. Otherwise, we return it.

Now fill the table. Amount one: only the coin one fits. One coin.

Amount two: one, plus the answer for one. Two coins.

Amount three: the coin three alone. One coin.

Amount four: the coin four alone. One coin.

Amount five: four plus one. Two coins.

Amount six. Using coin one leaves five, which needs two: three in total. Using coin three leaves three, which needs one: two in total. Using coin four leaves two, which needs two: three in total. The smallest is two.

We return two.

To check it: three plus three is six, with two coins, and no single coin is six.

There is one step per amount, per coin: O of amount times coins time. The table has one entry per amount: O of amount space. The direct search grows exponentially.

So that is Coin Change. The best way to make an amount is one coin, plus the best way to make the rest, and the table remembers every rest.

Follow for more if you want to really understand the problems interviews ask. Code included.
```

## Part 20 - Merge Intervals (LeetCode 56)

Example: [[8,10],[1,3],[2,6],[15,18],[5,7]] -> [[1,7],[8,10],[15,18]]

```
Today, LeetCode problem fifty six. Merge Intervals.

Here is the plan. Sort the intervals by where they start. Then one walk does the job. Each interval either overlaps the last merged interval and stretches it, or starts a new one.

The intervals are eight to ten, one to three, two to six, fifteen to eighteen, and five to seven. Two intervals overlap when one starts before the other ends. We want every overlapping group merged into one interval.

The direct way compares every pair, merges any two that overlap, and repeats until nothing changes. Five intervals already give ten pairs per round. The bottleneck is that, unsorted, any interval could overlap any other, so every pair must be checked, again and again.

Sorting changes that. Once the intervals are in order of their start, a new interval can only overlap the last merged interval. Every earlier merged interval ends before that one starts. So each interval needs exactly one comparison.

Sorted, they are one to three, two to six, five to seven, eight to ten, and fifteen to eighteen.

Now the code. It has two parts.

First, sort by start, and put the first interval into the merged list.

Second, the loop over the rest. Last is the final merged interval. If the new interval starts at or before last's end, they overlap, and last's end becomes the larger of the two ends. Otherwise, the new interval is added as a fresh one.

Now run it. Merged starts with one to three.

Two to six starts at two, before three. Overlap. The end becomes six: one to six.

Five to seven starts at five, before six. Overlap again. The end becomes seven: one to seven.

Eight to ten starts after seven. No overlap. It is added.

Fifteen to eighteen starts after ten. Added.

We return one to seven, eight to ten, and fifteen to eighteen.

To check it: one to three, two to six, and five to seven form one chain. Eight and fifteen both start after the group before them ends.

Notice the end is the larger of the two, not just the new one. If one to ten were followed by two to three, taking the new end would wrongly shrink it to three.

Sorting is O of n log n, and the walk is O of n, so O of n log n time. The merged list can hold n intervals: O of n space. The direct way was O of n squared, or worse.

So that is Merge Intervals. After sorting, a new interval can only touch the last one, so one comparison is enough.

Follow for more if you want to really understand the problems interviews ask. Code included.
```

## Part 21 - Rotting Oranges (LeetCode 994)

Example: [[2,1,1],[1,1,0],[0,1,1]] -> 4

```
Today, LeetCode problem nine hundred ninety four. Rotting Oranges.

Here is the plan. Put every rotten orange in a queue. Each minute, the oranges in the queue rot their fresh neighbours, and those newly rotten oranges become the next minute's queue. Count the minutes until nothing fresh is left.

The grid has three rows and three columns. Two is a rotten orange, one is fresh, and zero is empty. The top row is two, one, one. The middle row is one, one, zero. The bottom row is zero, one, one. Each minute, a rotten orange rots the fresh ones up, down, left, and right of it. We want the minutes until no fresh orange is left, or minus one if some can never rot.

The direct way scans the whole grid every minute, rots every fresh orange that touches a rotten one, and repeats. Here that is five scans of nine cells: forty five cell checks. On a large grid, that is O of cells squared. The bottleneck is that each scan looks at oranges that rotted long ago. Only the ones that rotted last minute can spread anything new.

So we only keep track of the newest rotten oranges. That moving edge is called the frontier. Spreading outward one layer at a time, from all the starting points together, is a multi source breadth first search.

Now the code. It has three parts.

First, the setup. Two loops look at every cell once. Rotten oranges go into the queue, and fresh ones are counted.

Second, a helper called rot. It takes a cell. If the cell is inside the grid and holds a fresh orange, it marks it rotten, lowers the fresh count, and adds it to the queue.

Third, the minute loop, which runs while the queue has oranges and fresh ones remain. We read the queue's length, so we only process this minute's oranges. Each one calls rot on its four neighbours. Then a minute is added. At the end, if nothing is fresh, we return the minutes. Otherwise, minus one.

Now run it. Six oranges are fresh, and one is rotten, in the top left corner.

Minute one. The corner rots the orange below it, and the one to its right. Four fresh left.

Minute two. Those two spread. The center rots, and so does the top right. Two fresh left.

Minute three. The center rots the orange below it. One fresh left.

Minute four. That orange rots the last one, in the bottom right. None left.

We return four.

To check it: the bottom right orange is the farthest from the corner. The shortest path to it, around the empty cells, takes four steps.

Notice that rot marks an orange the moment it is queued. So no orange is ever queued twice, and an orange rotted this minute does not spread until the next.

Each cell enters the queue at most once: O of rows times columns time. The queue can hold every cell: O of rows times columns space. The direct way was O of cells squared.

So that is Rotting Oranges. Start from every rotten orange at once, and spread one layer per minute.

Follow for more if you want to really understand the problems interviews ask. Code included.
```

## Part 22 - Course Schedule (LeetCode 207)

Example: 4 courses, prerequisites [[1,0],[2,0],[3,1],[3,2]] -> true; cycle [[0,1],[1,0]] -> false

```
Today, LeetCode problem two hundred seven. Course Schedule.

Here is the plan. For every course, count how many prerequisites it still needs. Take any course that needs none. Taking it lowers the count of every course that was waiting on it. If we manage to take every course this way, the schedule works. If we get stuck, there is a cycle.

There are four courses, zero to three. Course one needs course zero. Course two needs course zero. Course three needs both one and two. We want to know whether all four courses can be finished.

The direct way repeatedly scans every course, looking for one whose prerequisites are all taken, and takes it. Each scan checks every course and its prerequisites, and there can be as many scans as there are courses. The bottleneck is rescanning courses whose situation has not changed.

But a course only becomes available at one moment: when its last prerequisite is taken. So instead of rescanning, keep a count of missing prerequisites for each course, and a queue of the courses whose count is zero. This ordering is called a topological sort.

Now the code. It has three parts.

First, build the graph. After maps each course to the courses that depend on it. Needs counts each course's missing prerequisites.

Second, every course whose count is zero goes into the queue.

Third, the loop. Take a course from the queue, and count it as taken. For each course that depends on it, lower its count by one. If the count reaches zero, that course joins the queue. At the end, the answer is whether we took all the courses.

Now run it. The counts are zero, one, one, and two. Only course zero is ready.

Take zero. Courses one and two each lose a requirement. Both reach zero, and join the queue.

Take one. Course three goes from two to one. Not ready yet.

Take two. Course three reaches zero, and joins the queue.

Take three. Four courses taken, out of four. We return true.

To check it: zero, one, two, three is an order where every course comes after its prerequisites.

Now the failing case. If course zero needed course one, and course one needed course zero, neither count could ever reach zero. The queue starts empty, nothing is taken, and we return false. That is a cycle.

Every course and every prerequisite is handled once: O of courses plus prerequisites, in time and in space. The direct way could rescan the whole graph once for every course.

So that is Course Schedule. Take what is ready, let each course unlock what depends on it, and a cycle is whatever never unlocks.

Follow for more if you want to really understand the problems interviews ask. Code included.
```

## Part 23 - Top K Frequent Elements (LeetCode 347)

Example: [1, 1, 1, 2, 2, 3], k = 2 -> [1, 2]

```
Today, LeetCode problem three hundred forty seven. Top K Frequent Elements.

Here is the plan. Count how often each number appears. A count can never be bigger than the length of the array, so we make one bucket for every possible count, and drop each number into the bucket for its count. Then we walk the buckets from the highest count down, and stop once we have k numbers.

The numbers are one, one, one, two, two, three, and k is two. We want the two numbers that appear most often.

The direct way counts each number, then sorts the numbers by their counts, and takes the first k. Sorting is O of n log n. The bottleneck is that sorting puts every number in full order, when we only need the top k, and the counts are small whole numbers.

When the keys are small whole numbers, we do not need to compare them. We can use each count directly as a position. That is called bucket sort.

Now the code. It has three parts.

First, a counter that maps each number to how often it appears.

Second, a list of buckets, one for each count, from zero up to the array's length. Each number is appended to the bucket of its count.

Third, a loop over the counts, from the highest down to one. Each number found is added to the result, and as soon as the result holds k numbers, we return it.

Now run it. One appears three times, two appears twice, and three appears once. There are six numbers, so the buckets go from zero to six.

One goes into bucket three. Two goes into bucket two. Three goes into bucket one.

Walk down from six. Buckets six, five, and four are empty. Bucket three gives one. Bucket two gives two. That is k numbers. We return one and two.

To check it: one appears three times, and two appears twice. No other number appears more than once.

Counting is O of n. There are n plus one buckets, and every number lands in exactly one of them, so the walk is O of n too. O of n time, and O of n space. The direct way was O of n log n.

If an interviewer prefers, a heap of size k gives O of n log k. Buckets beat it, because the counts can never exceed n.

So that is Top K Frequent Elements. Counts are small whole numbers, so use them as positions instead of sorting.

Follow for more if you want to really understand the problems interviews ask. Code included.
```

## Part 24 - Minimum Window Substring (LeetCode 76)

Example: s = "AXBCAB", t = "ABC" -> "BCA"

```
Today, LeetCode problem seventy six. Minimum Window Substring.

Here is the plan. Slide a window over the string. Grow it on the right until it contains every character we need. Then shrink it from the left for as long as it still contains them, recording the smallest window seen. Then grow again.

The string is a, x, b, c, a, b. The target is a, b, c. We want the shortest stretch of the string that contains a, b, and c.

The direct way checks every substring. Six characters give twenty one substrings, and each one has to be counted. For a long string, that is O of n squared substrings, or more. The bottleneck is that neighbouring substrings are counted from scratch, though they differ by one character.

A window can be updated one character at a time instead. Adding a character on the right changes one count. Removing one on the left changes one count. We just need to know, at every moment, whether the window is complete.

For that, we keep two things. Need maps each character to how many more of it the window still owes. Missing is the total number of target characters still absent. When missing is zero, the window is valid.

Now the code. It has three parts.

First, the setup. Need is the count of the target's characters. Missing starts at the target's length. Left starts at zero, and the best window starts empty, with infinite length.

Second, the right edge walks over the string. If the window still owed this character, missing goes down by one. Either way, its need goes down. A character the target does not want simply goes below zero.

Third, while missing is zero, the window is valid. We record it if it is the smallest so far. Then we give back the leftmost character. Its need goes up by one, and if that need becomes positive, the window now owes it, so missing goes up. Left moves forward.

At the end, we return the best window, or an empty string if there never was one.

Now run it. A is needed. Missing two. X is not needed. B is needed. Missing one. C is needed. Missing zero.

The window a, x, b, c is valid, length four. Recorded. Drop a. Now a is owed again. Missing one.

A arrives on the right. Missing zero. The window x, b, c, a is valid, length four, no better. Drop x. X was extra, so nothing is owed. Still valid: b, c, a, length three. Recorded. Drop b. Missing one.

B arrives. The window c, a, b is valid, length three, but not shorter. Drop c. Missing one.

The string ends. We return b, c, a.

To check it: b, c, a contains all three, and no stretch of two characters can hold three different letters.

Each character enters the window once, and leaves it at most once: O of the string's length plus the target's length. The counts take O of the alphabet size in space. The direct way was O of n squared, or more.

So that is Minimum Window Substring. Grow until the window is complete, shrink while it stays complete, and two counts tell you which is which.

Follow for more if you want to really understand the problems interviews ask. Code included.
```

## Part 25 - LRU Cache (1 of 2): the design (LeetCode 146)

Example: capacity 2: put(1), put(2), get(1) -> 1, put(3) evicts 2, get(2) -> -1

```
Today, LeetCode problem one hundred forty six. LRU Cache. This problem gets two videos. This one is the design, and the next one builds it by hand.

Here is the plan. A cache with limited room must find any key instantly, and also know which key was used least recently. No single structure does both. A hash map finds keys. A linked list keeps the order of use. Python's OrderedDict is exactly those two joined together, so the whole cache takes a few lines.

The cache has room for two items. We put key one, then key two. We get key one. We put key three. Then we get key two. Least recently used means: when the cache is full, the item untouched for the longest time is removed. Both get and put must be O of one.

The direct way keeps a list of keys in order of use. Every get or put has to find the key in that list, and move it to the end. Finding it is a scan: O of n per operation. That scan is the bottleneck.

The fix is to let a hash map find the key, and to keep the order in a linked list, where a found item can be unlinked and moved to the end in constant time. An OrderedDict is a hash map whose keys are kept in a doubly linked list, so it gives us both.

Now the code. It has three parts.

First, the constructor stores the capacity, and an empty OrderedDict.

Second, get. If the key is missing, return minus one. Otherwise, move the key to the end, because it was just used, and return its value.

Third, put. If the key already exists, move it to the end. Store the value. If the cache is now over capacity, pop the item at the front, which is the least recently used.

Now run it. Put one. The order is one. Put two. The order is one, two.

Get one. It exists, so it moves to the end. The order is two, one. We return one.

Put three. The order is two, one, three. That is three items, one too many. The front item, two, is removed. The order is one, three.

Get two. It was evicted. We return minus one.

To check it: when three arrived, two was the item untouched for the longest time, so it was the one to go.

Get and put each do a constant number of map and list operations: O of one time. The cache holds at most its capacity: O of capacity space. The direct list was O of n per operation.

In an interview, you may be asked to build this without OrderedDict. That is the next video.

So that is the design of an LRU cache. A hash map to find, a linked list to order, and both updated together.

Follow for more if you want to really understand the problems interviews ask. Code included.
```

## Part 26 - LRU Cache (2 of 2): built by hand (LeetCode 146)

Example: same operations as Part 25 -> 1, -1

```
Today, LeetCode problem one hundred forty six again. LRU Cache, built by hand, without OrderedDict.

Here is the plan. Store each item in a node of a doubly linked list, with the newest at the front and the oldest at the back. A hash map points from each key to its node. To use an item, unlink its node and put it at the front. To evict, remove the node at the back. Every step is a few pointer changes.

The cache has room for two items. We put key one, put key two, get key one, put key three, and get key two. The same operations as last time, so the answers should be the same: one, then minus one.

Building it has one awkward part. Adding or removing at the very front or back usually needs special cases, for an empty list or a single node. We avoid them with two dummy nodes, a head and a tail, that are never removed. Every real node always sits between two other nodes. These dummies are called sentinel nodes.

Now the code. It has four parts.

First, the node. It holds a key, a value, and two arrows: prev and next. It keeps its key, so that when it is evicted, we know which map entry to delete.

Second, the constructor. It stores the capacity and an empty map, creates the head and the tail, and links them to each other.

Third, two helpers. Remove links a node's two neighbours to each other, which cuts the node out. Add front puts a node right after the head, with four arrow changes.

Fourth, get and put. Get returns minus one for a missing key. Otherwise, it removes the node, adds it at the front, and returns its value. Put removes any old node for that key, creates a new node, maps the key to it, and adds it at the front. If the map is now over capacity, the node just before the tail is the least recently used. It is removed from the list, and from the map.

Now run it. Put one. Head, one, tail. Put two. Two goes to the front: head, two, one, tail.

Get one. Its node is cut out, and added at the front: head, one, two, tail. We return one.

Put three. Head, three, one, two, tail. The map now holds three keys, more than two. The node before the tail is two. It is cut out, and key two is deleted from the map.

Get two. It is not in the map. We return minus one.

To check it: the answers match the OrderedDict version. One, then minus one.

Every operation is one map lookup and a few arrow changes: O of one time. The map and the list hold at most capacity items: O of capacity space.

So that is an LRU cache built by hand. Sentinels remove the edge cases, the map finds the node, and the list keeps the order.

Follow for more if you want to really understand the problems interviews ask. Code included.
```
