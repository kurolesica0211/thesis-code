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
Prince Heinrich of Prussia (German: Albert Wilhelm Heinrich; 14 August 1862 – 20 April 1929) was a younger brother of German Emperor and King of Prussia Wilhelm II and a Prince of Prussia.
Biography

Born in Berlin, Prince Heinrich was the third child and second son of eight children born to Crown Prince Frederick William (later Emperor Frederick III), and Victoria, Princess Royal (later Empress Victoria and in widowhood Empress Frederick), eldest daughter of the British Queen Victoria.
Henry was three years younger than his brother, the future Emperor William II (born 27 January 1859).
He was born on the same day as King Frederick William I "Soldier-King" of Prussia.
Early commands

As a Prussian prince, Henry quickly achieved command.
Squadron commands

From 1897, Prince Henry commanded several naval task forces; these included an improvised squadron that took part with the East Asia Squadron in consolidating and securing the German hold on the region of Kiaochow and the port of Tsingtao in 1898.
The prince's success was more of the diplomatic than the military variety; he became the first European potentate ever to be received at the Chinese imperial court.
From 1906 to 1909, Henry was commander of the High Seas Fleet.
I

At the beginning of World War I, Prince Henry was named as Commander-in-Chief of the Baltic Fleet.
After the end of hostilities with Russia, his mission was ended, and Prince Henry simply left active duty.
With the war's end and the dissolution of the monarchy in Germany, Prince Henry left the navy.
Family

On 24 May 1888, Henry married Princess Irene of Hesse and by Rhine, his first cousin.
His dying father, German Emperor Frederick III and his mother Empress Victoria were in attendance.
The marriage produced three children:


Their sons Waldemar and Heinrich were both hemophiliacs, a disease which they inherited through Irene from the maternal grandmother of both of their parents, Queen Victoria, who was a carrier.
Personality and private life

Henry received one of the first pilot's licenses in Germany, and was judged a spirited and excellent seaman.
A yachting enthusiast, Prince Henry became one of the first members of the Yacht Club of Kiel, established by a group of naval officers in 1887, and quickly became the club's patron.
Henry was interested in motor cars as well and supposedly invented a windshield wiper and, according to other sources, the car horn.
In his honor, the Prinz-Heinrich-Fahrt (Prince Heinrich Tour) was established in 1908, like the earlier Kaiserpreis a precursor to the German Grand Prix.
Henry and his brother William gave patronage to the Kaiserlicher Automobilclub (Imperial Automobile Club).
From 1911 to 1914 the British car makers Vauxhall Motors produced a model, the C-10, which was called the "Vauxhall Prince Henry" in his honour after initially being built for participation in the 1911 race.
After the German Revolution, Henry lived with his family in Hemmelmark near Eckernförde, in Schleswig-Holstein.
He popularized the Prince Henry cap, which is still worn, especially by older sailors.
In 1899, Henry received an honorary doctorate (Doctor of Engineering honoris causa) from the Technische Hochschule in Charlottenburg (now Technische Universität Berlin) .
Prince Henry died of throat cancer on 20 April 1929 in Hemmelmark.



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
  AssignClass (74a5ff21-3237-4990-b300-f0db3f3c1572)
 Call ID: 74a5ff21-3237-4990-b300-f0db3f3c1572
  Args:
    source: PrinceHeinrichOfPrussia
    type: :Man
  AssignClass (4e7234f4-2c53-43a3-b721-f930ba5e629d)
 Call ID: 4e7234f4-2c53-43a3-b721-f930ba5e629d
  Args:
    type: :Person
    source: PrinceHeinrichOfPrussia
  AddLiteral (d6cd6a11-f20f-49b1-9f8b-f3b203d04ed3)
 Call ID: d6cd6a11-f20f-49b1-9f8b-f3b203d04ed3
  Args:
    source: PrinceHeinrichOfPrussia
    literal_type: xsd:integer
    literal_value: 1862
    relation: :hasBirthYear
  AddLiteral (c97a91d8-38c6-463c-ae82-5ea1b648eda1)
 Call ID: c97a91d8-38c6-463c-ae82-5ea1b648eda1
  Args:
    relation: :hasDeathYear
    literal_value: 1929
    source: PrinceHeinrichOfPrussia
    literal_type: xsd:integer
  AssignClass (c85db883-7f8a-4b6d-ac38-394496e5ab4a)
 Call ID: c85db883-7f8a-4b6d-ac38-394496e5ab4a
  Args:
    type: :Man
    source: WilhelmII
  AssignClass (b62dcc27-3b3d-44b8-b006-85fcc7a4f003)
 Call ID: b62dcc27-3b3d-44b8-b006-85fcc7a4f003
  Args:
    source: WilhelmII
    type: :Person
  AddTriple (111d563d-1998-4dd9-b59e-0a5e91a845e1)
 Call ID: 111d563d-1998-4dd9-b59e-0a5e91a845e1
  Args:
    target: WilhelmII
    relation: :isBrotherOf
    source: PrinceHeinrichOfPrussia
  AddTriple (c23766e8-7f3e-478d-93e2-4211629062ae)
 Call ID: c23766e8-7f3e-478d-93e2-4211629062ae
  Args:
    source: WilhelmII
    target: PrinceHeinrichOfPrussia
    relation: :hasBrother
  AssignClass (94bfc903-291c-4920-8a4e-de25e55ff01b)
 Call ID: 94bfc903-291c-4920-8a4e-de25e55ff01b
  Args:
    source: FrederickIII
    type: :Man
  AssignClass (ab7e93ef-d7ae-4471-8bf3-c2e3d4fc9d15)
 Call ID: ab7e93ef-d7ae-4471-8bf3-c2e3d4fc9d15
  Args:
    source: FrederickIII
    type: :Person
  AssignClass (c577ad5e-f69f-4cb4-814f-c9e8c2318dbd)
 Call ID: c577ad5e-f69f-4cb4-814f-c9e8c2318dbd
  Args:
    type: :Ancestor
    source: FrederickIII
  AssignClass (c9ca6634-da5a-4c30-8ff8-e286e46f47e8)
 Call ID: c9ca6634-da5a-4c30-8ff8-e286e46f47e8
  Args:
    type: :Woman
    source: EmpressVictoria
  AssignClass (0d201cdf-a7e1-4654-a91d-ac86b8fbd4be)
 Call ID: 0d201cdf-a7e1-4654-a91d-ac86b8fbd4be
  Args:
    type: :Person
    source: EmpressVictoria
  AssignClass (61f4eb0a-b8a0-4a31-9dd2-43e6b55fd13b)
 Call ID: 61f4eb0a-b8a0-4a31-9dd2-43e6b55fd13b
  Args:
    type: :Ancestor
    source: EmpressVictoria
  AddTriple (94ffc4d4-76a3-4e32-9c44-204d4deae4e8)
 Call ID: 94ffc4d4-76a3-4e32-9c44-204d4deae4e8
  Args:
    source: PrinceHeinrichOfPrussia
    target: FrederickIII
    relation: :hasFather
  AddTriple (cb3485b9-af2a-402e-9c54-cf89e7978347)
 Call ID: cb3485b9-af2a-402e-9c54-cf89e7978347
  Args:
    relation: :hasMother
    target: EmpressVictoria
    source: PrinceHeinrichOfPrussia
  AssignClass (e3f80048-52bb-474a-a56e-a8a64e2cfb98)
 Call ID: e3f80048-52bb-474a-a56e-a8a64e2cfb98
  Args:
    source: QueenVictoria
    type: :Woman
  AssignClass (3e70fa81-f3dc-4da6-9bfa-e6fd6597670d)
 Call ID: 3e70fa81-f3dc-4da6-9bfa-e6fd6597670d
  Args:
    source: QueenVictoria
    type: :Person
  AssignClass (aaa578ec-61f4-4b28-9548-581e18225b29)
 Call ID: aaa578ec-61f4-4b28-9548-581e18225b29
  Args:
    type: :Ancestor
    source: QueenVictoria
  AddTriple (31a92c31-d679-4f51-9a3f-fe93c5cb02aa)
 Call ID: 31a92c31-d679-4f51-9a3f-fe93c5cb02aa
  Args:
    target: QueenVictoria
    relation: :hasMother
    source: EmpressVictoria
  AssignClass (5b1dba12-2372-4728-9565-ddaf59de1a5b)
 Call ID: 5b1dba12-2372-4728-9565-ddaf59de1a5b
  Args:
    source: PrincessIreneOfHesseAndByRhine
    type: :Woman
  AssignClass (5256e3e4-516a-4423-84c8-9160d0208a82)
 Call ID: 5256e3e4-516a-4423-84c8-9160d0208a82
  Args:
    type: :Person
    source: PrincessIreneOfHesseAndByRhine
  AddTriple (ccf5fbde-f4a4-4d8a-985f-ee52777f3460)
 Call ID: ccf5fbde-f4a4-4d8a-985f-ee52777f3460
  Args:
    relation: :hasRelation
    target: PrincessIreneOfHesseAndByRhine
    source: PrinceHeinrichOfPrussia
  AddLiteral (5cafd521-c007-4ea1-9dc4-db44c2d4d595)
 Call ID: 5cafd521-c007-4ea1-9dc4-db44c2d4d595
  Args:
    literal_value: 1888
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: PrinceHeinrichOfPrussia
  AssignClass (ecfe2225-726b-4f5f-92fb-33fca5ddfe7b)
 Call ID: ecfe2225-726b-4f5f-92fb-33fca5ddfe7b
  Args:
    type: :Man
    source: Waldemar
  AssignClass (708eaeba-c870-4e93-8b1b-abe0be7f6f3a)
 Call ID: 708eaeba-c870-4e93-8b1b-abe0be7f6f3a
  Args:
    source: Waldemar
    type: :Person
  AssignClass (d1a11d56-a5d7-4771-b4b9-cb013da30a82)
 Call ID: d1a11d56-a5d7-4771-b4b9-cb013da30a82
  Args:
    source: Heinrich_son
    type: :Man
  AssignClass (1c902dd3-5739-4fbc-962c-96d96cfffa38)
 Call ID: 1c902dd3-5739-4fbc-962c-96d96cfffa38
  Args:
    source: Heinrich_son
    type: :Person
  AddTriple (f42e850e-c54f-4131-8694-0c64ebe2ec63)
 Call ID: f42e850e-c54f-4131-8694-0c64ebe2ec63
  Args:
    target: Waldemar
    relation: :hasSon
    source: PrinceHeinrichOfPrussia
  AddTriple (aeae9ced-0977-458b-b6f4-6798086995b1)
 Call ID: aeae9ced-0977-458b-b6f4-6798086995b1
  Args:
    target: Heinrich_son
    relation: :hasSon
    source: PrinceHeinrichOfPrussia
  AddTriple (17ef6914-86f1-4185-96a6-5749157ea553)
 Call ID: 17ef6914-86f1-4185-96a6-5749157ea553
  Args:
    relation: :isChildOf
    target: PrinceHeinrichOfPrussia
    source: Waldemar
  AddTriple (411aa471-291d-4fba-bced-5995d2378a9f)
 Call ID: 411aa471-291d-4fba-bced-5995d2378a9f
  Args:
    source: Heinrich_son
    target: PrinceHeinrichOfPrussia
    relation: :isChildOf
  AddTriple (2648e8cf-b5f2-4984-bb51-1dc21330b0a1)
 Call ID: 2648e8cf-b5f2-4984-bb51-1dc21330b0a1
  Args:
    source: Waldemar
    target: PrincessIreneOfHesseAndByRhine
    relation: :hasMother
  AddTriple (f5c30092-c0b2-495e-90f8-25fff1b1d654)
 Call ID: f5c30092-c0b2-495e-90f8-25fff1b1d654
  Args:
    source: Heinrich_son
    relation: :hasMother
    target: PrincessIreneOfHesseAndByRhine
  Finish (8a885c8c-7cc0-411e-b0c6-2822713fd4e6)
 Call ID: 8a885c8c-7cc0-411e-b0c6-2822713fd4e6
  Args: