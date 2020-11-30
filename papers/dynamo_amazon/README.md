# Dynamo: Amazon's Highly Available Key Value Store

## System Design / System Architecture 


 Table 1: Summary and techniques sued in Dynamo and their advantages 

| Problem                            | Technique                                              | Advantage                                                                                                    |
| -------------                      | -------------                                          | -------------                                                                                                |
| Partitioning                       | Consistent Hashing                                     | Incremental Scalability                                                                                      |
| High Availability for writes       | Vector clocks with reconciliation during reads         | Version size is decoupled from update rates                                                                  |
| Handling temp failures             | Sloppy Quorom and hinted handoff                       | Provides high availability and durability guarantee when some of the replicas are not available              |
| Recovering from permanent failures | Anti entropy using merkle trees                        | Synchronizes divergent replicas in the background                                                            |
| Membership and failure detection   | Gossip based membership protocol and failure detection | Preserves symmetry and avoids having a centralized registry for storing membership and livenness information |

* Simple interface exposed through get and put operations 
* Applies MD5 hash to the key to determine the storage nodes 

### Partition Algorithm 
    * Relies on consistent hashing to distribute the load across multiple storage hosts 
    * The output range of the hash function is treated as a fixed circular ring 
    * Each node in the fixed circular ring is assigned, stochastically, a position
    * Consistent hashing advantage is the departure or arrival of a node only affects the neighbors 
    * The random assignment of nodes leads to a non uniform data and load distribution 
    * Dynamo addresses with virtual nodes   
        * Looks like a single node and can represent many nodes 
        * Asigned multiple positions in the ring
    * Virtual node advantages
        * If a node is unavailable there is another node that is evenly dispersed 
        * When a new node is available or another node is added, the data and laod is 
        evenly distrubuted 
        * Number of virtual nodes that a node is responsible for can be determained
        by its capacity.

### Replication
    * To achieve high availability and durability, Dynamo replicates its data to multiple host
    * Each data item is replicated at N hosts.
    * Each key k is assigned to a coordinator node, and the coordinator node 
    is responsible for the replication of data items that fall within the range 
    * Each coordinator node stores the key k locally. 
    * Preference list: the list of nodes responsible for a particular key. 
        * has unique node values 
    * To account for failures a preference list can have more than N nodes. 

### Data Versioning 
    * Dynamo provide eventual consistency 
    * Not all replicas may get the most up to date right before the next read. 
    * Some services should always preserve the past history
    * Dynamo treats each result of each modification as a new and immutable version. 
    * Dynamo uses vector clocks to capture causality of the same object 
    * Vector clock 
        * list of (node, couter pairs)
        * one vector clock can be associated with every version of the object.
    * One can determine whether objects are parallel branches or casual ordering 
        * by taking a lok at the counter 
        * if the first object is less than or equal to all nodes in the second clock
        then the first is an ancestor of the second
        * o/w the two are conflicting 
    * Objects that use the update command require that the object to modify is specified 
    * One issue that can arrive is that during reconciliation the vector clock may grow to big;
    however this is not an issue with dynamo as the writes are handled by the top n nodes in the list 
    ; top n healty nodes. 
    * Along with the (node, counter) pair dynamo stores the timestamp
    * Once the size of the vector clock reaches a threshold, the oldest is evicted 

### Execution of get and put operations 
    * A node handling a read or write is known as a coordinator node 
    * First n healthy nodes are used in the list ...
    * To  maintain consistency among replicas, dynamo uses a quorum system 
        * Protocol has two key configurable values R and W 
        * R is the min number of nodes that need to participate in a successful read operation 
        * W is the min number of nodes that need to participate in a successful write operation
        * R + W > N yiels a quorom like system 
        * Usually R and W set less than N to improve latency 

### Handling Failures: Hinted Handoff 
    * To solve the issue regarding unavailable servers or failure in network partitions 
    Dynamo uses a slooppy quorom, all read and writs are performed on the first N healthy nodes
    * Example 
        * If Node A is down during a write operation then a replica that would have normally lived
        in A will be sent to D. D will have a hint in its meta data that ssuggests which node 
        was intended as the recepient. Nodes that have hinted replicas will keep them in a local db 
        * Transfer from A to D happens when A has recoveredi
    * Write request is rejected if all nodes in the system are unavailable 
    * Objects replicated among multiple data centers 

### Handling permanent failures: Replica synchronization 
    * Hinted handoff works best is the system membership is low and node failures are transient
    * Dynamo implements anti entropy merkle trees to keep replicas in sync 
        * merkle tree is where the leaves of the hashes are the values of the indv keys 
        * Parent nodes highere are their respective children 
    * Merkle tree advantage 
        * individual branches can be checked without requiring to check the entire tree
        * if the hash of two roots are the same then there requires no sync 
        * nodes may exchange hash values until it receives the leaves 
    * How it is used in dynamo 
        * each node creates a seperate merkle tree for each key range 
        * disadvantage is taht when the key ranges change when a node leaves or joins the ring 
        then the tree(s) require to be recalculated

### Membership and Failure detection 
    * A node outage is usually temporary and should not reaquire any rebalancing 
        * Admin must handle this 
    * Gossip protocl propagtes membership changes ...
    * Seeds are nodes that are discovered via external mechanism and are known to all nodes
    * All nodes reconcile membership with a seed 
