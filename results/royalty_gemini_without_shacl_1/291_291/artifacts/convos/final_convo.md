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
Princess Xenia Georgievna of Russia (22 August 1903 – 17 September 1965) was the younger daughter of Grand Duke George Mihailovich of Russia and Princess Maria Georgievna of Greece and Denmark.
She is known for recognizing Anna Anderson as Grand Duchess Anastasia.
Youth

Xenia and her older sister Princess Nina Georgievna, who was born in 1901, left Russia in 1914 to spend the war years in England with their mother.
In 1919, her father, his brother Grand Duke Nicholas Mikhailovich, and their cousins Grand Duke Paul Alexandrovich and Grand Duke Dmitry Konstantinovich, were executed by a Bolshevik firing squad in St. Petersburg.
Anna Anderson controversy

In the summer of 1927, Xenia involved herself in the Anna Anderson/Anastasia Tchaikovsky affair by telephoning Gleb Botkin (son of imperial physician Eugene Botkin, who had been murdered along with the former tsar and his family in 1918) with an invitation for Anna to live as a guest at their luxurious estate in New York's Oyster Bay.
Xenia explains her hospitality: "I had heard that Botkin was arranging to bring 'the invalid' to the United States through a newspaper organization.
As children, Xenia and her sister Nina had played frequently with the two youngest daughters of Tsar Nicholas II, Grand Duchesses Maria Nikolaevna and Anastasia Nikolaevna, as well as the youngest child and only boy, Tsarevitch Alexei.
Through her father, Xenia was Anastasia's second cousin, once removed and through her mother they were second cousins.
According to Xenia, Anastasia "cheated at games, kicked, scratched, pulled hair, and generally knew how to make herself obnoxious.
"


Xenia was on a cruise with her husband William in the West Indies at the time of Anna's arrival in New York.
She had arranged for Anna to stay with Annie Burr Jennings, a friend of Xenia's who lived in a Park Avenue townhouse.
Upon her return, Xenia sneaked unannounced into Annie Jennings's crowded salon to observe Anna.
After watching Anna offer her hand to Gleb Botkin, Xenia declared that she knew she was watching an equal.
"


Xenia recognized Anna Anderson as the Grand Duchess Anastasia at once, asserting that Anna was herself at all times, never giving the slightest impression of playing a part.
The two remained great friends for life even after Anna Anderson had to leave Xenia's home after quarreling.
Then her treatment of the Grand Duchess Xenia, sister of the last Tsar, led to a quarrel with William Leeds, who turned her out of the house.
Pierre Gilliard, tutor for the five children of Tsar Nicholas II from 1905 to 1918, pointed out that Princess Xenia had last seen her second cousin when Xenia was 10 and Anastasia was 12.
Xenia responded that she did not recognize Anastasia visually, but felt she was qualified to tell the difference between a member of the Romanov family and a "Polish peasant woman."
Anderson bore a strong family resemblance to Tsarina Alexandra's family and her moodiness and temper also reminded Xenia of her cousin Anastasia.
Prince Dmitri, son of Grand Duchess Xenia, wrote about what Princess Xenia had stated,


Xenia's irresponsible statement should be somehow refuted ...
We know she left Russia in 1914 aged 10 years old, I also know that Nina (her sister) and Xenia never saw Uncle Nicky's family very often, and when they did see them that was when they were very young.
Personal life

Xenia married twice.
At age 18 she married William Bateman Leeds Jr. (19 September 1902 – 31 December 1971), the son and heir of the American tin magnate William B. Leeds Sr. and the stepson of Xenia's maternal uncle Prince Christopher of Greece and Denmark, through his marriage to William’s mother, the former Nonie Stewart Leeds.
Xenia and William had a daughter on 25 February 1925, Nancy Helen Marie Leeds.
Xenia and William Leeds divorced in 1930.
Xenia's second marriage was with Herman Jud (1911–1987), whom she married at Glen Cove, New York, on 10 August 1946.
Death

Princess Xenia Georgievna died on 17 September 1965, aged 62, survived by her second husband and by her daughter, Nancy Leeds Wynkoop, and by granddaughter Alexandra.



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
  AssignClass (34b07d0b-8399-4629-8ea6-9136755dd029)
 Call ID: 34b07d0b-8399-4629-8ea6-9136755dd029
  Args:
    type: :Woman
    source: Princess_Xenia_Georgievna_of_Russia
  AssignClass (3af1ce4c-7239-4baa-8df2-b949d3befc1f)
 Call ID: 3af1ce4c-7239-4baa-8df2-b949d3befc1f
  Args:
    type: :Person
    source: Princess_Xenia_Georgievna_of_Russia
  AddLiteral (6a2d6fd6-c22a-4afd-87f5-59c4d9314336)
 Call ID: 6a2d6fd6-c22a-4afd-87f5-59c4d9314336
  Args:
    source: Princess_Xenia_Georgievna_of_Russia
    literal_value: 1903
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (acd63f28-6b32-4256-8510-8ea84bfad755)
 Call ID: acd63f28-6b32-4256-8510-8ea84bfad755
  Args:
    literal_type: xsd:integer
    source: Princess_Xenia_Georgievna_of_Russia
    relation: :hasDeathYear
    literal_value: 1965
  AssignClass (7204c5cd-3d7f-47c6-ab91-c81b4bfe8679)
 Call ID: 7204c5cd-3d7f-47c6-ab91-c81b4bfe8679
  Args:
    type: :Man
    source: Grand_Duke_George_Mihailovich_of_Russia
  AssignClass (a5c028f1-34e0-43b4-a4af-574cc41d8192)
 Call ID: a5c028f1-34e0-43b4-a4af-574cc41d8192
  Args:
    type: :Person
    source: Grand_Duke_George_Mihailovich_of_Russia
  AddTriple (042cada5-11d0-478d-b727-551ed3d6ca5c)
 Call ID: 042cada5-11d0-478d-b727-551ed3d6ca5c
  Args:
    target: Princess_Xenia_Georgievna_of_Russia
    relation: :isFatherOf
    source: Grand_Duke_George_Mihailovich_of_Russia
  AssignClass (5f80a9bb-a56c-479d-9632-ce335b0eb659)
 Call ID: 5f80a9bb-a56c-479d-9632-ce335b0eb659
  Args:
    type: :Woman
    source: Princess_Maria_Georgievna_of_Greece_and_Denmark
  AssignClass (ad41e3e7-5c20-47d4-a66b-c8adc2a98264)
 Call ID: ad41e3e7-5c20-47d4-a66b-c8adc2a98264
  Args:
    type: :Person
    source: Princess_Maria_Georgievna_of_Greece_and_Denmark
  AddTriple (9a67548f-b90d-4f9f-a36d-9c9af632b9f1)
 Call ID: 9a67548f-b90d-4f9f-a36d-9c9af632b9f1
  Args:
    relation: :isMotherOf
    source: Princess_Maria_Georgievna_of_Greece_and_Denmark
    target: Princess_Xenia_Georgievna_of_Russia
  AssignClass (dafe8458-b585-4640-a8e2-69ac73c0b803)
 Call ID: dafe8458-b585-4640-a8e2-69ac73c0b803
  Args:
    type: :Woman
    source: Princess_Nina_Georgievna
  AssignClass (757c07d8-e8ff-4533-ab35-c554b9386817)
 Call ID: 757c07d8-e8ff-4533-ab35-c554b9386817
  Args:
    type: :Person
    source: Princess_Nina_Georgievna
  AddTriple (6bed8c7d-3d02-46eb-9170-d7b2355bfd8d)
 Call ID: 6bed8c7d-3d02-46eb-9170-d7b2355bfd8d
  Args:
    relation: :isSisterOf
    source: Princess_Nina_Georgievna
    target: Princess_Xenia_Georgievna_of_Russia
  AddTriple (c2f03465-f61b-42b3-9949-93ac4a6f53c3)
 Call ID: c2f03465-f61b-42b3-9949-93ac4a6f53c3
  Args:
    target: Princess_Maria_Georgievna_of_Greece_and_Denmark
    relation: :hasMother
    source: Princess_Nina_Georgievna
  AddTriple (4b7de0aa-d789-4b68-87cf-a9ca6ca2a9c4)
 Call ID: 4b7de0aa-d789-4b68-87cf-a9ca6ca2a9c4
  Args:
    relation: :hasFather
    source: Princess_Nina_Georgievna
    target: Grand_Duke_George_Mihailovich_of_Russia
  AssignClass (540c768d-7eff-4901-b34f-76afc108513d)
 Call ID: 540c768d-7eff-4901-b34f-76afc108513d
  Args:
    type: :Man
    source: Grand_Duke_Nicholas_Mikhailovich
  AssignClass (a971e32d-d1c3-42bd-8663-430d28a0efeb)
 Call ID: a971e32d-d1c3-42bd-8663-430d28a0efeb
  Args:
    type: :Person
    source: Grand_Duke_Nicholas_Mikhailovich
  AddTriple (31ebea41-1834-4a56-97d7-a346580f7b3e)
 Call ID: 31ebea41-1834-4a56-97d7-a346580f7b3e
  Args:
    target: Grand_Duke_George_Mihailovich_of_Russia
    source: Grand_Duke_Nicholas_Mikhailovich
    relation: :isBrotherOf
  AssignClass (f376ab8a-935d-4859-8ee6-71288c5d4663)
 Call ID: f376ab8a-935d-4859-8ee6-71288c5d4663
  Args:
    type: :Man
    source: William_Bateman_Leeds_Jr
  AssignClass (1ff1d0e5-7447-4acf-ac1a-f2a2d8fbe704)
 Call ID: 1ff1d0e5-7447-4acf-ac1a-f2a2d8fbe704
  Args:
    type: :Person
    source: William_Bateman_Leeds_Jr
  AddLiteral (06367f1a-a018-482c-b0c1-8e6dfe309354)
 Call ID: 06367f1a-a018-482c-b0c1-8e6dfe309354
  Args:
    source: William_Bateman_Leeds_Jr
    relation: :hasBirthYear
    literal_value: 1902
    literal_type: xsd:integer
  AddLiteral (19ed6c40-1e3f-4c6c-9683-bf3262781985)
 Call ID: 19ed6c40-1e3f-4c6c-9683-bf3262781985
  Args:
    literal_type: xsd:integer
    source: William_Bateman_Leeds_Jr
    literal_value: 1971
    relation: :hasDeathYear
  AddTriple (737ada1e-fbf0-441c-9104-8bca5a7b2abf)
 Call ID: 737ada1e-fbf0-441c-9104-8bca5a7b2abf
  Args:
    relation: :hasRelation
    source: Princess_Xenia_Georgievna_of_Russia
    target: William_Bateman_Leeds_Jr
  AssignClass (879458d7-6b87-4b89-9526-6db912087cca)
 Call ID: 879458d7-6b87-4b89-9526-6db912087cca
  Args:
    type: :Woman
    source: Nancy_Helen_Marie_Leeds
  AssignClass (0eade3d4-79f5-4de0-b815-54aee4c78218)
 Call ID: 0eade3d4-79f5-4de0-b815-54aee4c78218
  Args:
    type: :Person
    source: Nancy_Helen_Marie_Leeds
  AddTriple (c923518c-6577-4b89-a851-4669ab3a49a8)
 Call ID: c923518c-6577-4b89-a851-4669ab3a49a8
  Args:
    target: Princess_Xenia_Georgievna_of_Russia
    source: Nancy_Helen_Marie_Leeds
    relation: :isDaughterOf
  AddTriple (dde0996a-228d-4ca0-97fe-0ef6c1c75797)
 Call ID: dde0996a-228d-4ca0-97fe-0ef6c1c75797
  Args:
    target: William_Bateman_Leeds_Jr
    source: Nancy_Helen_Marie_Leeds
    relation: :isDaughterOf
  AssignClass (e644a56f-69f3-47f8-a8b4-4c0dd6937a01)
 Call ID: e644a56f-69f3-47f8-a8b4-4c0dd6937a01
  Args:
    type: :Man
    source: Herman_Jud
  AssignClass (17d23f00-2c10-4233-8cb0-ba4266a26e34)
 Call ID: 17d23f00-2c10-4233-8cb0-ba4266a26e34
  Args:
    type: :Person
    source: Herman_Jud
  AddLiteral (32afc8e8-e1b2-45ea-ae19-1004054de863)
 Call ID: 32afc8e8-e1b2-45ea-ae19-1004054de863
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1911
    source: Herman_Jud
  AddLiteral (5817af65-a74a-4c6e-b13f-acfe230511dc)
 Call ID: 5817af65-a74a-4c6e-b13f-acfe230511dc
  Args:
    source: Herman_Jud
    literal_value: 1987
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (ad87849f-f947-48e5-bd03-17c79f4e844d)
 Call ID: ad87849f-f947-48e5-bd03-17c79f4e844d
  Args:
    target: Herman_Jud
    relation: :hasRelation
    source: Princess_Xenia_Georgievna_of_Russia
  Finish (e8c8be78-8b3b-4b7a-aaff-8c5920118869)
 Call ID: e8c8be78-8b3b-4b7a-aaff-8c5920118869
  Args: