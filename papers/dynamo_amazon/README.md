# Dynamo: Amazon's Highly Available Key Value Store

## System Design


 Table 1: Summary and techniques sued in Dynamo and their advantages 

| Problem                            | Technique                                              | Advantage                                                                                                    |
| -------------                      | -------------                                          | -------------                                                                                                |
| Partitioning                       | Consistent Hashing                                     | Incremental Scalability                                                                                      |
| High Availability for writes       | Vector clocks with reconciliation during reads         | Version size is decoupled from update rates                                                                  |
| Handling temp failures             | Sloppy Quorom and hinted handoff                       | Provides high availability and durability guarantee when some of the replicas are not available              |
| Recovering from permanent failures | Anti entropy using merkle trees                        | Synchronizes divergent replicas in the background                                                            |
| Membership and failure detection   | Gossip based membership protocol and failure detection | Preserves symmetry and avoids having a centralized registry for storing membership and livenness information |



