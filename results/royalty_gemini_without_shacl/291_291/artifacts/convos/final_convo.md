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
  AssignClass (92ff8ead-f93f-4ccc-821c-e3c316b60b23)
 Call ID: 92ff8ead-f93f-4ccc-821c-e3c316b60b23
  Args:
    type: :Woman
    source: :XeniaGeorgievna
  AssignClass (f41f6ae6-7bda-4c2d-9f8f-abde0ec128fc)
 Call ID: f41f6ae6-7bda-4c2d-9f8f-abde0ec128fc
  Args:
    source: :XeniaGeorgievna
    type: :Person
  AddLiteral (9b095231-f926-40d1-b72a-d5fbbc7dd593)
 Call ID: 9b095231-f926-40d1-b72a-d5fbbc7dd593
  Args:
    literal_value: 1903
    source: :XeniaGeorgievna
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (1bb250ae-f5e9-47fd-8446-5cff2d555bfa)
 Call ID: 1bb250ae-f5e9-47fd-8446-5cff2d555bfa
  Args:
    literal_value: 1965
    literal_type: xsd:integer
    source: :XeniaGeorgievna
    relation: :hasDeathYear
  AssignClass (dcf951fa-b60c-4275-a3fe-6a01a406328c)
 Call ID: dcf951fa-b60c-4275-a3fe-6a01a406328c
  Args:
    source: :GeorgeMihailovich
    type: :Man
  AssignClass (72f9871b-1a2a-4339-8cf7-1af2e82a3b9d)
 Call ID: 72f9871b-1a2a-4339-8cf7-1af2e82a3b9d
  Args:
    source: :GeorgeMihailovich
    type: :Person
  AssignClass (68f47c5b-b834-444d-a674-ec283368da35)
 Call ID: 68f47c5b-b834-444d-a674-ec283368da35
  Args:
    type: :Woman
    source: :MariaGeorgievna
  AssignClass (590fa403-9b3c-4ced-95e8-b84c03a4f564)
 Call ID: 590fa403-9b3c-4ced-95e8-b84c03a4f564
  Args:
    source: :MariaGeorgievna
    type: :Person
  AddTriple (498da19b-c578-4d9f-b42f-c5bac9a0c785)
 Call ID: 498da19b-c578-4d9f-b42f-c5bac9a0c785
  Args:
    relation: :hasFather
    source: :XeniaGeorgievna
    target: :GeorgeMihailovich
  AddTriple (3b2e887b-f046-4020-aeac-00f9f573ad19)
 Call ID: 3b2e887b-f046-4020-aeac-00f9f573ad19
  Args:
    source: :XeniaGeorgievna
    relation: :hasMother
    target: :MariaGeorgievna
  AssignClass (746f7126-197e-4628-ab14-f76193961db7)
 Call ID: 746f7126-197e-4628-ab14-f76193961db7
  Args:
    type: :Woman
    source: :NinaGeorgievna
  AssignClass (827ea5bf-4208-4d62-986f-061ceb73edc5)
 Call ID: 827ea5bf-4208-4d62-986f-061ceb73edc5
  Args:
    type: :Person
    source: :NinaGeorgievna
  AddTriple (6b72a2ae-f854-4bf8-ba47-872a542e1076)
 Call ID: 6b72a2ae-f854-4bf8-ba47-872a542e1076
  Args:
    target: :NinaGeorgievna
    source: :XeniaGeorgievna
    relation: :isSisterOf
  AddTriple (b7976540-e9d7-41f7-9e5b-205d98e00e93)
 Call ID: b7976540-e9d7-41f7-9e5b-205d98e00e93
  Args:
    relation: :hasFather
    source: :NinaGeorgievna
    target: :GeorgeMihailovich
  AddTriple (1e5cf9a3-de31-45e5-8472-ac8b8ca2e102)
 Call ID: 1e5cf9a3-de31-45e5-8472-ac8b8ca2e102
  Args:
    target: :MariaGeorgievna
    relation: :hasMother
    source: :NinaGeorgievna
  AssignClass (0e8889f4-e2ca-4968-b71d-5a73a8ed6913)
 Call ID: 0e8889f4-e2ca-4968-b71d-5a73a8ed6913
  Args:
    type: :Man
    source: :NicholasMikhailovich
  AssignClass (3fbd7ca1-d326-4c76-937e-1861c2cdf06b)
 Call ID: 3fbd7ca1-d326-4c76-937e-1861c2cdf06b
  Args:
    source: :NicholasMikhailovich
    type: :Person
  AddTriple (2bc9d5ce-809a-45a0-8b83-491ec8156590)
 Call ID: 2bc9d5ce-809a-45a0-8b83-491ec8156590
  Args:
    source: :NicholasMikhailovich
    relation: :isBrotherOf
    target: :GeorgeMihailovich
  AssignClass (7e317eb4-7509-4ea0-82d9-c256555c4eb1)
 Call ID: 7e317eb4-7509-4ea0-82d9-c256555c4eb1
  Args:
    source: :WilliamBatemanLeedsJr
    type: :Man
  AssignClass (18343605-1880-4925-af71-ed46ba24d3f5)
 Call ID: 18343605-1880-4925-af71-ed46ba24d3f5
  Args:
    source: :WilliamBatemanLeedsJr
    type: :Person
  AddTriple (7b133fe7-3ef6-4a2b-8874-4bae37eb11c0)
 Call ID: 7b133fe7-3ef6-4a2b-8874-4bae37eb11c0
  Args:
    relation: :hasRelation
    source: :XeniaGeorgievna
    target: :WilliamBatemanLeedsJr
  AssignClass (7f1b78e4-c09b-4aa1-8c37-daf1528ec693)
 Call ID: 7f1b78e4-c09b-4aa1-8c37-daf1528ec693
  Args:
    source: :NancyHelenMarieLeeds
    type: :Woman
  AssignClass (358e3f46-e339-4e92-83ee-93a1cd8b5ccc)
 Call ID: 358e3f46-e339-4e92-83ee-93a1cd8b5ccc
  Args:
    source: :NancyHelenMarieLeeds
    type: :Person
  AddTriple (4684dd52-8f2f-45b0-908d-4fac67a78175)
 Call ID: 4684dd52-8f2f-45b0-908d-4fac67a78175
  Args:
    target: :XeniaGeorgievna
    relation: :isDaughterOf
    source: :NancyHelenMarieLeeds
  AddTriple (d2972295-7475-4bb9-9f8a-7649c53e3681)
 Call ID: d2972295-7475-4bb9-9f8a-7649c53e3681
  Args:
    target: :WilliamBatemanLeedsJr
    relation: :isDaughterOf
    source: :NancyHelenMarieLeeds
  AssignClass (b85aab7c-3bf7-465f-ad38-7d317cca3fc6)
 Call ID: b85aab7c-3bf7-465f-ad38-7d317cca3fc6
  Args:
    type: :Man
    source: :HermanJud
  AssignClass (8f52a4a9-55d1-48cc-aa19-bd6f0ddaebe0)
 Call ID: 8f52a4a9-55d1-48cc-aa19-bd6f0ddaebe0
  Args:
    source: :HermanJud
    type: :Person
  AddTriple (7ad0bb12-205d-48ff-a817-82909ae2a0b7)
 Call ID: 7ad0bb12-205d-48ff-a817-82909ae2a0b7
  Args:
    target: :HermanJud
    source: :XeniaGeorgievna
    relation: :hasRelation
  Finish (3a1801b9-d176-442b-938b-3bc29dd6d243)
 Call ID: 3a1801b9-d176-442b-938b-3bc29dd6d243
  Args: