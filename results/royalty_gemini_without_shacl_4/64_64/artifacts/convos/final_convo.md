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
Prince Andrew of Greece and Denmark (Greek: Ανδρέας, romanized: Andréas; 2 February  1882 – 3 December 1944) was the seventh child and fourth son of King George I and Queen Olga of Greece.
He was a grandson of King Christian IX of Denmark and the father of Prince Philip, Duke of Edinburgh.
He was a prince of Greece and Denmark, both by virtue of his patrilineal descent.
A career soldier, Andrew began military training at an early age, and was commissioned as an officer in the Greek army.
In 1913, his father was assassinated and Andrew's elder brother Constantine became king.
Constantine's neutrality policy during World War I led to his abdication, and most of the royal family, including Andrew, was exiled.
On their return a few years later, Andrew saw service as Major General in the Greco-Turkish War (1919–1922), but the war went badly for Greece, and Andrew was blamed, in part, for the loss of Greek territory.
He was exiled for a second time in 1922, and spent most of the rest of his life in France.
By 1930, Andrew was estranged from his wife, Princess Alice of Battenberg.
His only son, Philip, served in the British navy during World War II, while all four of his daughters were married to Germans, three of whom had Nazi connections.
Separated from his wife and son by the effects of the war, Andrew died in Monte Carlo in 1944.
Early life

Andrew was born on 2 February 1882 at the Tatoi Palace, just north of Athens.
He was the fourth son of George I of Greece and Olga Constantinovna of Russia.
A member of the House of Schleswig-Holstein-Sonderburg-Glücksburg, Andrew held the title of prince in both Greece and Denmark, as his father was a younger son of Christian IX of Denmark.
He was in the line of succession to the Greek throne.
In addition to his native Greek, Andrew learnt Danish, German, French, English, and Russian.
Despite his near-sightedness, Andrew joined the army as a cavalry officer in May 1901.
Marriage

In 1902, Andrew met Princess Alice of Battenberg during his stay in London on the occasion of the coronation of Edward VII, who was his uncle-by-marriage and her grand-uncle.
Princess Alice was a daughter of Prince Louis of Battenberg and Princess Victoria of Hesse and by Rhine, King Edward's niece.
They fell in love, and the following year, on 6 October 1903, Andrew married Alice in a civil wedding at Darmstadt.
Prince and Princess Andrew had five children, all of whom later had children of their own.
Early career

In 1909, the political situation in Greece led to a coup d'état, as the Athens government refused to support the Cretan parliament, which had called for the union of Crete (still nominally part of the Ottoman Empire) with the Greek mainland.
A group of dissatisfied officers formed a Greek nationalist Military League and demanded, among other reforms, the removal of royal princes from the army, which led to Andrew's resignation from the army and the rise to power of Eleftherios Venizelos.
A few years later, at the outbreak of the Balkan Wars in 1912, Andrew was reinstated in the army as a lieutenant colonel in the 3rd Cavalry Regiment, and placed in command of a field hospital.
During the war, his father was assassinated and Andrew inherited a villa on the island of Corfu, Mon Repos, as well as an annuity of £4,000.
In 1914, Andrew (like many European princes) held honorary military posts in both the German and Russian empires, as well as Prussian, Russian, Danish and Italian knighthoods.
During World War I, Andrew continued to visit Britain, despite veiled accusations in the British House of Commons that he was a German agent.
By June 1917, the King's neutrality policy had become so untenable that he abdicated and the Greek royal family were forced into exile.
For the next few years, most of the Greek royal family lived in Switzerland.
Exile from Greece

For three years, Constantine's second son, Alexander, was king of Greece, until his early death from an infection due to a monkey bite.
Constantine was restored to the throne, and Andrew was once again reinstated in the army, this time as a major-general.
Andrew was given command of the II Army Corps during the Battle of the Sakarya, which effectively halted the Greek advance in the Greco-Turkish War (1919–1922).
Andrew had little respect for his superior officers, whom he considered incompetent.
Refusing to put his men in undue danger (suffering lack of food and ammunition), Andrew followed his own battle plan, much to the dismay of the commanding general, Anastasios Papoulas.
Relieved of his chief of staff, and given a dressing-down by Papoulas, in September Andrew asked to be removed from command but Papoulas refused.
Andrew's troops were forced to retreat.
The Greek defeat in Asia Minor in August 1922 led to the 11 September 1922 Revolution, during which Andrew was arrested, court-martialed, and found guilty of "disobeying an order" and "acting on his own initiative" during the battle of the previous year.
British diplomats assumed that Andrew was also in mortal danger.
Andrew, though spared, was banished for life and his family fled into exile aboard a British cruiser, HMS Calypso.
The family settled at Saint-Cloud on the outskirts of Paris, in a small house lent to them by Andrew's wealthy sister-in-law, Princess George of Greece.
In 1930, Andrew published a book entitled Towards Disaster: The Greek Army in Asia Minor in 1921, in which he defended his actions during the Battle of the Sakarya, but he essentially lived a life of enforced retirement, despite only being in his forties.
Alice suffered a nervous breakdown and was institutionalised in Switzerland.
Their daughters married and settled in Germany, separated from Andrew, and Philip was sent to school in Britain, where he was brought up by his mother's British relatives.
Andrew went to live in the South of France.
On the French Riviera, Andrew lived in a small apartment, or hotel rooms, or on board a yacht with Countess Andrée de La Bigne.
His marriage to Alice was effectively over, and after her recovery and release, she returned to Greece.
In 1936, his sentence of exile was quashed by emergency laws, which also restored land and annuities to the King.
Andrew returned to Greece for a brief visit that May.
The following year, his pregnant daughter Cecilie, his son-in-law and two of his grandchildren were killed in an air accident at Ostend; he travelled to London to meet up with his sixteen-year-old son Prince Philip and they went together to Darmstadt where he met Alice for the first time in six years at the funeral.
During World War II, he found himself essentially trapped in Vichy France, while his son, Prince Philip, fought on the side of the British.
They were unable to see or even correspond with one another.
Andrew's three surviving sons-in-law fought on the German side: Prince Christoph of Hesse was a member of the Nazi Party and the Waffen-SS; Berthold, Margrave of Baden, was invalided out of the Wehrmacht in 1940 after an injury in France; Prince Gottfried of Hohenlohe-Langenburg served on the Eastern Front and was dismissed after the 20 July plot.
For five years, Andrew saw neither his wife nor his son.
Death and burial

Andrew died aged 62 in the closing months of the war in Europe on 3 December 1944 in the Hotel Metropole, Monte Carlo, of heart failure and arteriosclerosis.
He was at first buried in the Russian Orthodox church in Nice, but in 1946 his remains were transferred, by the Greek cruiser Averof, to the royal cemetery at Tatoi Palace, near Athens.
Prince Philip and then-private secretary, Mike Parker, travelled to Monte Carlo to collect items belonging to his father from Andrée de La Bigne; among these items: a signet ring which the Prince wore from then onwards, an ivory shaving brush he took to using, and some clothes that he had altered to fit him.
Andrew left to his only son seven-tenths of his estate, but he also left behind a debt of £17,500, leading Philip's maternal grandmother, Victoria Mountbatten, Marchioness of Milford Haven, to complain bitterly of the extravagance the Greek prince had been led into by his French mistress.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
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

ns2:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns1:Variable .

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

:y a ns1:Variable .

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

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (c25fc70d-4e11-405c-8ed9-5c84e8ca059f)
 Call ID: c25fc70d-4e11-405c-8ed9-5c84e8ca059f
  Args:
    type: :Man
    source: Prince_Andrew_of_Greece_and_Denmark
  AssignClass (c84d406b-77d5-4c6c-9706-eb727967f900)
 Call ID: c84d406b-77d5-4c6c-9706-eb727967f900
  Args:
    source: Prince_Andrew_of_Greece_and_Denmark
    type: :Person
  AddLiteral (ce1cfc70-2068-4595-abda-ec6131f395a6)
 Call ID: ce1cfc70-2068-4595-abda-ec6131f395a6
  Args:
    source: Prince_Andrew_of_Greece_and_Denmark
    relation: :hasBirthYear
    literal_value: 1882
    literal_type: xsd:integer
  AddLiteral (060f2685-3898-4078-95d3-8268c2df6181)
 Call ID: 060f2685-3898-4078-95d3-8268c2df6181
  Args:
    source: Prince_Andrew_of_Greece_and_Denmark
    literal_value: 1944
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (b1ebaa5d-b839-4f67-bfb2-81568978002e)
 Call ID: b1ebaa5d-b839-4f67-bfb2-81568978002e
  Args:
    source: King_George_I_of_Greece
    type: :Man
  AssignClass (0eb4d20d-398a-4347-b7be-4ec9c52aeda1)
 Call ID: 0eb4d20d-398a-4347-b7be-4ec9c52aeda1
  Args:
    source: King_George_I_of_Greece
    type: :Person
  AssignClass (aa2938f3-c70c-479e-89e4-7806b8717d21)
 Call ID: aa2938f3-c70c-479e-89e4-7806b8717d21
  Args:
    type: :Woman
    source: Queen_Olga_of_Greece
  AssignClass (3f86c704-7454-4520-9b27-58e99c87245c)
 Call ID: 3f86c704-7454-4520-9b27-58e99c87245c
  Args:
    source: Queen_Olga_of_Greece
    type: :Person
  AddTriple (59c19bec-0e17-4151-aed0-aad6066af506)
 Call ID: 59c19bec-0e17-4151-aed0-aad6066af506
  Args:
    relation: :hasFather
    source: Prince_Andrew_of_Greece_and_Denmark
    target: King_George_I_of_Greece
  AddTriple (f7d88e61-c5aa-4c58-82c7-4346e3bf831e)
 Call ID: f7d88e61-c5aa-4c58-82c7-4346e3bf831e
  Args:
    relation: :hasMother
    source: Prince_Andrew_of_Greece_and_Denmark
    target: Queen_Olga_of_Greece
  AssignClass (589ab6fa-18d7-4215-af1f-729cf0537521)
 Call ID: 589ab6fa-18d7-4215-af1f-729cf0537521
  Args:
    source: King_Christian_IX_of_Denmark
    type: :Man
  AssignClass (7c04215d-b298-406c-90a5-721bad85d27e)
 Call ID: 7c04215d-b298-406c-90a5-721bad85d27e
  Args:
    source: King_Christian_IX_of_Denmark
    type: :Person
  AddTriple (2f88ff99-d3be-46c3-b926-aec77c7d2ecb)
 Call ID: 2f88ff99-d3be-46c3-b926-aec77c7d2ecb
  Args:
    source: Prince_Andrew_of_Greece_and_Denmark
    target: King_Christian_IX_of_Denmark
    relation: :hasAncestor
  AssignClass (6243c688-7988-4d43-9e80-2ed722d27662)
 Call ID: 6243c688-7988-4d43-9e80-2ed722d27662
  Args:
    source: Prince_Philip_Duke_of_Edinburgh
    type: :Man
  AssignClass (1c01ab23-c22c-4c06-b31a-991cc899d658)
 Call ID: 1c01ab23-c22c-4c06-b31a-991cc899d658
  Args:
    source: Prince_Philip_Duke_of_Edinburgh
    type: :Person
  AddTriple (231d6734-92be-4596-b730-bb5dde34c544)
 Call ID: 231d6734-92be-4596-b730-bb5dde34c544
  Args:
    relation: :hasFather
    source: Prince_Philip_Duke_of_Edinburgh
    target: Prince_Andrew_of_Greece_and_Denmark
  AssignClass (c013ddc2-e093-4cc2-b878-046efc8bc282)
 Call ID: c013ddc2-e093-4cc2-b878-046efc8bc282
  Args:
    source: Princess_Alice_of_Battenberg
    type: :Woman
  AssignClass (91ba1884-f3d1-4836-a96d-3f187d58b96c)
 Call ID: 91ba1884-f3d1-4836-a96d-3f187d58b96c
  Args:
    type: :Person
    source: Princess_Alice_of_Battenberg
  AddLiteral (22439e14-e4fc-4a64-8710-c91381409ca3)
 Call ID: 22439e14-e4fc-4a64-8710-c91381409ca3
  Args:
    source: Prince_Andrew_of_Greece_and_Denmark
    literal_type: xsd:integer
    literal_value: 1903
    relation: :hasMarriageYear
  AddTriple (a632e859-17f5-4814-afa5-d45e6874423b)
 Call ID: a632e859-17f5-4814-afa5-d45e6874423b
  Args:
    relation: :hasMother
    target: Princess_Alice_of_Battenberg
    source: Prince_Philip_Duke_of_Edinburgh
  AssignClass (00770a48-98d0-42f5-8fb8-1d3c63df5f73)
 Call ID: 00770a48-98d0-42f5-8fb8-1d3c63df5f73
  Args:
    type: :Man
    source: Constantine_King_of_Greece
  AssignClass (9d06cdff-e455-43ed-a4b3-ab144fcbded9)
 Call ID: 9d06cdff-e455-43ed-a4b3-ab144fcbded9
  Args:
    type: :Person
    source: Constantine_King_of_Greece
  AddTriple (856e4bfd-71c6-440a-b0df-88fd2c3f64cf)
 Call ID: 856e4bfd-71c6-440a-b0df-88fd2c3f64cf
  Args:
    target: Constantine_King_of_Greece
    source: Prince_Andrew_of_Greece_and_Denmark
    relation: :hasBrother
  AssignClass (f915f1d7-ba16-4e19-94b3-52e4a2eb49df)
 Call ID: f915f1d7-ba16-4e19-94b3-52e4a2eb49df
  Args:
    type: :Man
    source: Prince_Louis_of_Battenberg
  AssignClass (15d1752a-f0dc-4ec9-9313-f137eb3994ab)
 Call ID: 15d1752a-f0dc-4ec9-9313-f137eb3994ab
  Args:
    type: :Person
    source: Prince_Louis_of_Battenberg
  AssignClass (ce73a44a-fdef-40b0-96f5-34602ac5ea46)
 Call ID: ce73a44a-fdef-40b0-96f5-34602ac5ea46
  Args:
    source: Princess_Victoria_of_Hesse_and_by_Rhine
    type: :Woman
  AssignClass (916319e5-4664-4d03-b16f-11b290d55a23)
 Call ID: 916319e5-4664-4d03-b16f-11b290d55a23
  Args:
    type: :Person
    source: Princess_Victoria_of_Hesse_and_by_Rhine
  AddTriple (1ee28477-6d25-4bbb-9992-f92048e7e998)
 Call ID: 1ee28477-6d25-4bbb-9992-f92048e7e998
  Args:
    relation: :hasFather
    source: Princess_Alice_of_Battenberg
    target: Prince_Louis_of_Battenberg
  AddTriple (167b9a21-872c-4af3-9bd6-ec92d60a1cb6)
 Call ID: 167b9a21-872c-4af3-9bd6-ec92d60a1cb6
  Args:
    source: Princess_Alice_of_Battenberg
    target: Princess_Victoria_of_Hesse_and_by_Rhine
    relation: :hasMother
  AssignClass (70ba6980-a167-414c-8570-99413ec6081d)
 Call ID: 70ba6980-a167-414c-8570-99413ec6081d
  Args:
    source: Alexander_King_of_Greece
    type: :Man
  AssignClass (59af96a4-cf3f-4285-8557-a2422da60dd9)
 Call ID: 59af96a4-cf3f-4285-8557-a2422da60dd9
  Args:
    source: Alexander_King_of_Greece
    type: :Person
  AddTriple (297217aa-1d17-4508-86c0-89f73ee20e25)
 Call ID: 297217aa-1d17-4508-86c0-89f73ee20e25
  Args:
    target: Constantine_King_of_Greece
    source: Alexander_King_of_Greece
    relation: :hasFather
  AssignClass (72da22be-7a3b-4d08-9a21-fa070db293ae)
 Call ID: 72da22be-7a3b-4d08-9a21-fa070db293ae
  Args:
    source: Cecilie
    type: :Woman
  AssignClass (679e17e9-81e9-4c3d-a4a7-129f8952907b)
 Call ID: 679e17e9-81e9-4c3d-a4a7-129f8952907b
  Args:
    source: Cecilie
    type: :Person
  AddTriple (48a90cc5-949a-497f-bd0c-cd36804ce5d1)
 Call ID: 48a90cc5-949a-497f-bd0c-cd36804ce5d1
  Args:
    source: Cecilie
    target: Prince_Andrew_of_Greece_and_Denmark
    relation: :hasFather
  AddTriple (40fc767c-f1db-4895-9f2e-4749599971d8)
 Call ID: 40fc767c-f1db-4895-9f2e-4749599971d8
  Args:
    relation: :hasMother
    source: Cecilie
    target: Princess_Alice_of_Battenberg
  Finish (4cec1780-ee22-40ee-b693-93b22f1a6973)
 Call ID: 4cec1780-ee22-40ee-b693-93b22f1a6973
  Args: