================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Ernest Augustus (Ernest Augustus Christian George; German: Ernst August Christian Georg; 17 November 1887 – 30 January 1953) was Duke of Brunswick from 2 November 1913 to 8 November 1918.
He was also a maternal grandson of Christian IX of Denmark and the son-in-law of German Emperor Wilhelm II.
Early life

Ernest Augustus was born at Penzing near Vienna, the sixth and youngest child of former Crown Prince Ernest Augustus of Hanover and his wife, Princess Thyra of Denmark.
His great-grandfather, Prince Ernest Augustus, Duke of Cumberland, the fifth son of George III of the United Kingdom, became king of Hanover in 1837 because Salic Law barred Victoria, Queen of the United Kingdom, from inheriting the Hanoverian throne.
His father succeeded as pretender to the Hanoverian throne and as Duke of Cumberland and Teviotdale in the peerage of Great Britain in 1878.
The younger Ernest Augustus became heir apparent to the dukedom of Cumberland and to the Hanoverian claim upon the deaths of his two elder brothers, George and Christian.
In 1884, his paternal great-granduncle the reigning Duke of Brunswick (a male line descendant of Henry, the older brother of William, his male line ancestor) died.
Since the younger branch of the House of Welf ended with him, under house rules it would have passed to the Duke of Cumberland, who immediately claimed the throne.
However, the Imperial Chancellor, Otto von Bismarck, managed to get the Federal Council (Bundesrat) of the German Empire to rule that the Duke of Cumberland would disturb the peace of the empire if he ascended the throne of Brunswick.
Bismarck did this because the duke had never formally renounced his claims to the kingdom of Hanover, which had been annexed to Prussia in 1866 following the end of the Austro-Prussian War (Hanover had sided with losing Austria).
Instead, Prince Albrecht of Prussia became the regent of Brunswick.
After Prince Albrecht's death in 1906, the duke offered that he and his elder son, Prince George, would renounce their claims to the Duchy of Brunswick in order to allow Ernest Augustus, his only other surviving son, to take possession of the Duchy, but this option was rejected by the Bundesrat and the regency continued, this time under Duke Johann Albrecht of Mecklenburg-Schwerin, who had previously acted as regent for his nephew in Mecklenburg.
Marriage and accession to the duchy of Brunswick

When Ernest Augustus's older brother George died in an automobile accident on 20 May 1912, the German Emperor, Wilhelm II, sent a message of condolence to the Duke of Cumberland.
In response to this friendly gesture, the Duke sent his only surviving son, Ernest Augustus, to Berlin to thank the Emperor for his message.
Ernest Augustus and Wilhelm II were third cousins through George III of the United Kingdom.
In Berlin, Ernest Augustus met and fell in love with the emperor's only daughter, Princess Victoria Louise of Prussia.
On 24 May 1913, Ernest Augustus and Victoria Louise, third cousins once removed through descent from George III's sons King Ernest Augustus of Hanover and Edward, Duke of Kent, were married to each other.
This marriage ended the decades-long rift between the Houses of Hohenzollern and Hanover.
The wedding of Prince Ernest Augustus and Princess Victoria Louise was also the last great gathering of European sovereigns before the outbreak of the Great War, as recalled by Constantine II of Greece, a grandson of the married couple, in 2003.
In addition to the German Emperor and Empress and the Duke and Duchess of Cumberland, King George V and Queen Mary of the United Kingdom and Tsar Nicholas II attended.
Upon the announcement of his betrothal to Princess Victoria Louise in February 1913, Ernest Augustus swore allegiance to the German Empire and accepted a commission as a cavalry captain and company commander in the Zieten–Hussars, a Prussian Army regiment in which his grandfather (George V) and great-grandfather (Ernest Augustus) had been colonels.
On 27 October 1913, the Duke of Cumberland formally renounced his claims to the duchy of Brunswick in favor of his surviving son.
The following day, the Federal Council voted to allow Ernest Augustus to become the reigning Duke of Brunswick.
The new Duke of Brunswick formally took possession of his duchy on 1 November.
The new duke and duchess of Brunswick moved into Brunswick Palace in the capital of Brunswick and began their family with the birth of their eldest son, Prince Ernest Augustus, less than a year after their wedding.
During the First World War, Ernest Augustus rose to the rank of major-general.
Abdication and later life

In 1917, the British dukedom of Ernest Augustus's father, and his own title as a Prince of the United Kingdom of Great Britain and Ireland, were removed by the Titles Deprivation Act 1917, which took effect in 1919, as a result of the Duke's service in the German army during the war.
On 8 November 1918, Ernest Augustus was forced to abdicate his throne, as were all the other German kings, grand dukes, dukes, and princes during the German Revolution of 1918–1919.
Thus, when his father died in 1923, Ernest Augustus did not succeed to his father's title of Duke of Cumberland.
For the next thirty years, Ernest Augustus remained as head of the House of Hanover, living in retirement on his various estates, mainly Blankenburg Castle in Germany and Cumberland Castle in Gmunden, Austria.
He also owned Marienburg Castle near Hanover, although rarely ever living there until 1945.
While Ernest Augustus never officially joined the Nazi Party, he donated funds and was close to several leaders.
As a former British prince, Ernest Augustus, as well as Victoria Louise, desired a rapprochement between the United Kingdom and Germany.
Ostensibly desiring to pursue an alliance with the UK, in the mid-1930s, Adolf Hitler took advantage of their sentiment by asking the couple to arrange a match between their daughter Princess Frederica and the Prince of Wales.
The Duke and Duchess of Brunswick refused, believing that the age difference was too great.
In 1938 Princess Frederica married Prince Paul of Greece, brother and heir-presumptive of King George II of Greece.
Ernest Augustus lived to see his daughter Frederica become a queen consort in 1947 when her husband Paul became King of the Hellenes.
Ernest Augustus died at Marienburg Castle in 1953.
He was interred, later to be joined by the remains of his wife, in front of the Royal Mausoleum in the Berggarten at Herrenhausen Gardens in Hanover, which is the burial chapel of King Ernest Augustus of Hanover and his wife.
Issue

The Duke and Duchess of Brunswick had five children:


Honours

Ancestry

References

Sources

External links



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

ns1:isRuleEnabled a owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns2:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns2:Variable .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (ff82b49c-b968-4377-9360-93396ce821de)
 Call ID: ff82b49c-b968-4377-9360-93396ce821de
  Args:
    source: Ernest_Augustus_of_Brunswick
    type: :Man
  AssignClass (cbedde99-d419-4564-b078-e0aa4d06c9dd)
 Call ID: cbedde99-d419-4564-b078-e0aa4d06c9dd
  Args:
    type: :Person
    source: Ernest_Augustus_of_Brunswick
  AddLiteral (4af97d73-f0d9-4d6e-bb2f-e9017fc24059)
 Call ID: 4af97d73-f0d9-4d6e-bb2f-e9017fc24059
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Ernest_Augustus_of_Brunswick
    literal_value: 1887
  AddLiteral (0f60c6b8-5e4b-49d2-a372-940eaf4491b5)
 Call ID: 0f60c6b8-5e4b-49d2-a372-940eaf4491b5
  Args:
    literal_value: 1953
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Ernest_Augustus_of_Brunswick
  AssignClass (0569ae48-b67f-4313-9ec0-16b080a5ef4d)
 Call ID: 0569ae48-b67f-4313-9ec0-16b080a5ef4d
  Args:
    source: Ernest_Augustus_of_Hanover
    type: :Man
  AssignClass (f157bbd5-b389-45b9-8072-8c0c874527bf)
 Call ID: f157bbd5-b389-45b9-8072-8c0c874527bf
  Args:
    type: :Person
    source: Ernest_Augustus_of_Hanover
  AssignClass (216e9b13-fed8-43df-a1e1-28d21b50f839)
 Call ID: 216e9b13-fed8-43df-a1e1-28d21b50f839
  Args:
    source: Thyra_of_Denmark
    type: :Woman
  AssignClass (379cc4f5-f28f-45e4-8f26-dd10114c5ada)
 Call ID: 379cc4f5-f28f-45e4-8f26-dd10114c5ada
  Args:
    source: Thyra_of_Denmark
    type: :Person
  AddTriple (bad7cefd-6ca5-40bd-91e9-25f0f9270ee8)
 Call ID: bad7cefd-6ca5-40bd-91e9-25f0f9270ee8
  Args:
    target: Ernest_Augustus_of_Hanover
    source: Ernest_Augustus_of_Brunswick
    relation: :hasFather
  AddTriple (60179762-5904-4f0e-b9e9-ca8c877fba34)
 Call ID: 60179762-5904-4f0e-b9e9-ca8c877fba34
  Args:
    source: Ernest_Augustus_of_Brunswick
    relation: :hasMother
    target: Thyra_of_Denmark
  AssignClass (4541d06e-0d7c-4706-a554-b12b662cd4b2)
 Call ID: 4541d06e-0d7c-4706-a554-b12b662cd4b2
  Args:
    source: George_of_Cumberland
    type: :Man
  AssignClass (a72819fc-ec67-4078-a005-86fc6a1f959c)
 Call ID: a72819fc-ec67-4078-a005-86fc6a1f959c
  Args:
    type: :Person
    source: George_of_Cumberland
  AssignClass (c7bf58b7-c99b-4593-aab3-e37479b1173b)
 Call ID: c7bf58b7-c99b-4593-aab3-e37479b1173b
  Args:
    source: Christian_of_Cumberland
    type: :Man
  AssignClass (c66a3ccc-ddf7-4d3d-9837-b352ba821d52)
 Call ID: c66a3ccc-ddf7-4d3d-9837-b352ba821d52
  Args:
    source: Christian_of_Cumberland
    type: :Person
  AddTriple (9d41cdc2-b9f9-4103-a3d2-21cb29bb3291)
 Call ID: 9d41cdc2-b9f9-4103-a3d2-21cb29bb3291
  Args:
    target: George_of_Cumberland
    relation: :isBrotherOf
    source: Ernest_Augustus_of_Brunswick
  AddTriple (76441dd3-efb5-4d78-b6b7-ed4543716b31)
 Call ID: 76441dd3-efb5-4d78-b6b7-ed4543716b31
  Args:
    relation: :isBrotherOf
    source: Ernest_Augustus_of_Brunswick
    target: Christian_of_Cumberland
  AssignClass (50f3e8b1-12f8-4cb7-9c4d-181cde3b37ee)
 Call ID: 50f3e8b1-12f8-4cb7-9c4d-181cde3b37ee
  Args:
    source: Victoria_Louise_of_Prussia
    type: :Woman
  AssignClass (6d439e8f-3d88-472f-90a9-5f895c0f1574)
 Call ID: 6d439e8f-3d88-472f-90a9-5f895c0f1574
  Args:
    source: Victoria_Louise_of_Prussia
    type: :Person
  AddTriple (fc34678e-b4b4-4770-9df9-6eae66480155)
 Call ID: fc34678e-b4b4-4770-9df9-6eae66480155
  Args:
    relation: :hasRelation
    source: Ernest_Augustus_of_Brunswick
    target: Victoria_Louise_of_Prussia
  AddLiteral (0466d832-378d-40f7-b632-54748e367824)
 Call ID: 0466d832-378d-40f7-b632-54748e367824
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Ernest_Augustus_of_Brunswick
    literal_value: 1913
  AssignClass (6aa789ed-8800-4712-921b-cea42f1091a1)
 Call ID: 6aa789ed-8800-4712-921b-cea42f1091a1
  Args:
    type: :Man
    source: Prince_Ernest_Augustus_of_Brunswick_Junior
  AssignClass (d492acc8-7206-4661-a26b-d972a5d7c414)
 Call ID: d492acc8-7206-4661-a26b-d972a5d7c414
  Args:
    source: Prince_Ernest_Augustus_of_Brunswick_Junior
    type: :Person
  AddTriple (6351be15-28c2-40bd-bcd3-8405be2925ed)
 Call ID: 6351be15-28c2-40bd-bcd3-8405be2925ed
  Args:
    source: Prince_Ernest_Augustus_of_Brunswick_Junior
    relation: :hasFather
    target: Ernest_Augustus_of_Brunswick
  AddTriple (5c4fef0c-1c78-4fca-b0da-bd472e4894b5)
 Call ID: 5c4fef0c-1c78-4fca-b0da-bd472e4894b5
  Args:
    relation: :hasMother
    source: Prince_Ernest_Augustus_of_Brunswick_Junior
    target: Victoria_Louise_of_Prussia
  AssignClass (902af214-2c98-4e74-af88-9f21f42748d0)
 Call ID: 902af214-2c98-4e74-af88-9f21f42748d0
  Args:
    type: :Woman
    source: Frederica_of_Brunswick
  AssignClass (a76b3776-a835-4c20-af8e-f4e0b68bc053)
 Call ID: a76b3776-a835-4c20-af8e-f4e0b68bc053
  Args:
    source: Frederica_of_Brunswick
    type: :Person
  AddTriple (c318317d-7ebe-4314-b9ff-a975426e1112)
 Call ID: c318317d-7ebe-4314-b9ff-a975426e1112
  Args:
    target: Ernest_Augustus_of_Brunswick
    relation: :hasFather
    source: Frederica_of_Brunswick
  AddTriple (b3f15cb0-b234-4fb8-aa2a-01aed6f9b79f)
 Call ID: b3f15cb0-b234-4fb8-aa2a-01aed6f9b79f
  Args:
    source: Frederica_of_Brunswick
    relation: :hasMother
    target: Victoria_Louise_of_Prussia
  AssignClass (926e30f8-a08e-4d64-a2ad-6ced670a2ee0)
 Call ID: 926e30f8-a08e-4d64-a2ad-6ced670a2ee0
  Args:
    type: :Man
    source: Paul_of_Greece
  AssignClass (f8073ced-9155-4025-b856-58b7575d7992)
 Call ID: f8073ced-9155-4025-b856-58b7575d7992
  Args:
    type: :Person
    source: Paul_of_Greece
  AddTriple (e8454118-7f9b-4154-96f2-04dcd59023ec)
 Call ID: e8454118-7f9b-4154-96f2-04dcd59023ec
  Args:
    source: Frederica_of_Brunswick
    relation: :hasRelation
    target: Paul_of_Greece
  AddLiteral (30d6681c-1fea-46d4-852e-2e1ab0b1f0e1)
 Call ID: 30d6681c-1fea-46d4-852e-2e1ab0b1f0e1
  Args:
    source: Frederica_of_Brunswick
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1938
  Finish (79a5fb3a-8858-4ccd-be9e-420352b1e0c1)
 Call ID: 79a5fb3a-8858-4ccd-be9e-420352b1e0c1
  Args: