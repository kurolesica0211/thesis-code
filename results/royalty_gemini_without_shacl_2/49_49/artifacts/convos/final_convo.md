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
Frederik IX (Christian Frederik Franz Michael Carl Valdemar Georg; 11 March 1899 – 14 January 1972) was King of Denmark from 1947 to 1972.
Frederik was born into the House of Glücksburg during the reign of his great-grandfather King Christian IX.
He was the first child of Prince Christian of Denmark and Princess Alexandrine of Mecklenburg-Schwerin (later King Christian X and Queen Alexandrine).
In 1935, he married Princess Ingrid of Sweden.
During Nazi Germany's occupation of Denmark, Frederik acted as regent from 1942 until 1943 on behalf of his father, who had suffered a horseback riding accident in October 1942.
Frederik became king on his father's death in April 1947.
During Frederik's reign, Danish society changed rapidly, the welfare state was expanded and, as a consequence of the booming economy of the 1960s, women entered the labour market.
The modernization brought new demands on the monarchy and Frederik's role as a constitutional monarch.
Frederik died in 1972, and was succeeded by his eldest daughter, Margrethe II.


Birth and family

Frederik was born on 11 March 1899 at his parents' country residence, the Sorgenfri Palace, located on the shores of the small river Mølleåen in Kongens Lyngby north of Copenhagen on the island of Zealand in Denmark, during the reign of his great-grandfather King Christian IX.
His father was Prince Christian of Denmark (later King Christian X), the eldest son of Crown Prince Frederik and Princess Louise of Sweden (later King Frederik VIII and Queen Louise).
His mother was Alexandrine of Mecklenburg-Schwerin, the eldest daughter of Frederick Francis III, Grand Duke of Mecklenburg-Schwerin and Grand Duchess Anastasia Mikhailovna of Russia.
The young prince had 21 godparents: Christian IX of Denmark (his paternal great-grandfather); Crown Prince Frederik of Denmark (his paternal grandfather); the Dowager Grand Duchess Anastasia of Mecklenburg-Schwerin (his maternal grandmother); Grand Duke Michael Nikolaevich of Russia (his maternal great-grandfather); Dowager Grand Duchess Marie of Mecklenburg-Schwerin (his maternal step-great-grandmother); Prince Carl of Denmark (his paternal uncle); Princess Thyra of Denmark (his paternal aunt); Frederick Francis IV, Grand Duke of Mecklenburg-Schwerin (his maternal uncle); George I of Greece (his paternal great-uncle); Albert Edward, Prince of Wales (his paternal great-uncle by marriage); Ernest August, Duke of Cumberland (his paternal great-uncle by marriage); Grand Duke Alexander Mikhailovich of Russia (his maternal great-uncle); his first cousins once removed, Nicholas II of Russia, George, Duke of York, Prince George of Greece and Denmark and Georg Wilhelm, Hereditary Prince of Hanover; Crown Prince Constantine and Crown Princess Sophia of Greece (his first cousin once removed, and his wife); his paternal great-granduncles, Prince Johann of Schleswig-Holstein-Sonderburg-Glücksburg and King Oscar II of Sweden and Norway; and Crown Prince Gustaf and Crown Princess Victoria of Sweden (his first cousin twice removed and his wife).
Frederik's only sibling, Knud, was born one year after Frederik.
The family lived in apartments in Christian VIII's Palace at Amalienborg Palace in Copenhagen, in Sorgenfri Palace near the capital and in a summer residence, Marselisborg Palace in Aarhus in Jutland, which Frederik's parents had received as a wedding present from the people of Denmark in 1898.
Early life

Christian IX died on 29 January 1906, and Frederik's grandfather Crown Prince Frederik succeeded him as King Frederik VIII.
Frederik's father became crown prince, and Frederik moved up to second in line to the throne.
Just six years later, on 14 May 1912, King Frederik VIII died, and Frederik's father ascended the throne as King Christian X. Frederik himself became crown prince.
On 1 December 1918, as the Danish–Icelandic Act of Union recognized Iceland as a fully sovereign state in personal union with Denmark through a common monarch, Frederik also became crown prince of Iceland (where his name was officially spelled Friðrik).
Frederik was educated at the Royal Danish Naval Academy (breaking with Danish royal tradition by choosing a naval instead of an army career) and the University of Copenhagen.
In addition, with his love of music, Frederik was an able piano player and conductor.
Marriage and issue

In the 1910s, Alexandrine considered the two youngest daughters of her cousin Tsar Nicholas II, Grand Duchesses Maria and Anastasia Nikolaevna of Russia, as possible wives for Frederik until the execution of the Romanov family in 1918.
In 1922, Frederik was engaged to Princess Olga of Greece and Denmark, his double second cousin, through King Christian IX of Denmark and the other through Frederick Francis II.
They never wed.


Instead, on 15 March 1935, a few days after his 36th birthday, his engagement to Princess Ingrid of Sweden (1910–2000), a daughter of Crown Prince Gustaf Adolf (later King Gustaf VI Adolf of Sweden) and his first wife, Princess Margaret of Connaught, was announced.
Frederik and Ingrid were related in several ways.
In descent from Oscar I of Sweden and Leopold, Grand Duke of Baden, they were double third cousins.
In descent from Paul I of Russia, Frederik was a fourth cousin of Ingrid's mother.
Their wedding was one of the greatest media events of the day in Sweden in 1935, and among the wedding guests were the King and Queen of Denmark, the King and Queen of Belgium and the Crown Prince and Crown Princess of Norway.
Upon their return to Denmark, the couple were given Frederik VIII's Palace at Amalienborg Palace in Copenhagen as their primary residence and Gråsten Palace in Northern Schleswig as a summer residence.
Their daughters are:


Reign

From 1942 until 1943, Frederik acted as regent on behalf of his father who was temporarily incapacitated after a fall from his horse in October 1942.
On 20 April 1947, Christian X died, and Frederik succeeded to the throne.
Frederik IX's reign saw great change.
In other words, Denmark became a modern country, which meant new demands on the monarchy.
Changes to the Act of Succession

As King Frederik IX and Queen Ingrid had no sons, it was expected that the king's younger brother, Prince Knud, would inherit the throne, in accordance with Denmark's succession law (Royal Ordinance of 1853).
As a result, his eldest daughter, Margrethe, became heir presumptive.
Death and funeral

Shortly after Frederik delivered his New Year's address on 31 December 1971, he became ill with flu-like symptoms.
He was succeeded by his eldest daughter, Margrethe II.
Following his death, Frederik's coffin was transported to his home at Amalienborg Palace, where it stood until 18 January, when it was moved to the chapel at Christiansborg Palace.
There, the coffin was placed on castrum doloris, a ceremony largely unchanged since introduced at the burial of Frederik III in 1670, and the last remaining royal ceremony where the Danish Crown Regalia is used.
The gun carriage was pulled by 48 seamen and was escorted by honor guards from the Danish Army, Air Force, and Navy, as well as honor guards from France, Sweden, the United Kingdom, and the United States.
Queen Ingrid survived her husband by 28 years.
Legacy

In 1934, the Crown Prince Frederik Range in Greenland was named after him when it was first mapped by Sir Martin Lindsay during the British Trans-Greenland Expedition.
On 20 April 1982, a statue of King Frederik IX dressed in the uniform of an admiral was unveiled by the Copenhagen harbour on the 35th anniversary of his accession to the throne in 1947 and in the tenth year after his death.
Folktale

In the southern city of Sønderborg, Frederik has a dish named after himself.
The dish is called "Kong Fiddes livret" (King Frederik's favorite).
The name Fidde is a common diminutive nickname for people named Frederik in the southern parts of Denmark.
The dish is supposedly one that was regularly served to Frederik on his birthday at Gråsten Palace.



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
  AssignClass (f4ac3343-a2a9-4558-b680-5885d3ce6be2)
 Call ID: f4ac3343-a2a9-4558-b680-5885d3ce6be2
  Args:
    source: :Frederik_IX
    type: :Man
  AssignClass (f3b1f779-a412-43b5-afbe-2e1574167814)
 Call ID: f3b1f779-a412-43b5-afbe-2e1574167814
  Args:
    source: :Frederik_IX
    type: :Person
  AddLiteral (7672f9eb-7745-4c72-a56c-068a4ce3ade2)
 Call ID: 7672f9eb-7745-4c72-a56c-068a4ce3ade2
  Args:
    literal_value: Christian Frederik Franz Michael Carl Valdemar Georg
    relation: :alsoKnownAs
    source: :Frederik_IX
    literal_type: xsd:string
  AddLiteral (ee4eeb32-3492-4213-9ddc-dc97d2267227)
 Call ID: ee4eeb32-3492-4213-9ddc-dc97d2267227
  Args:
    literal_type: xsd:positiveInteger
    literal_value: 1899
    source: :Frederik_IX
    relation: :hasBirthYear
  AddLiteral (2d860679-d3c5-4b96-83d2-61e1cce966f9)
 Call ID: 2d860679-d3c5-4b96-83d2-61e1cce966f9
  Args:
    literal_value: 1972
    relation: :hasDeathYear
    source: :Frederik_IX
    literal_type: xsd:positiveInteger
  AssignClass (e754483b-2226-4077-b5fb-1c3b82e2fc9d)
 Call ID: e754483b-2226-4077-b5fb-1c3b82e2fc9d
  Args:
    source: :Christian_X
    type: :Man
  AssignClass (21583af7-6214-4b88-91d1-0bbd0634569a)
 Call ID: 21583af7-6214-4b88-91d1-0bbd0634569a
  Args:
    type: :Person
    source: :Christian_X
  AssignClass (6537d2bb-43f4-4028-b406-a39cc21ddd6b)
 Call ID: 6537d2bb-43f4-4028-b406-a39cc21ddd6b
  Args:
    type: :Woman
    source: :Alexandrine_of_Mecklenburg-Schwerin
  AssignClass (f44dd8f2-bf14-4c44-b98d-8ce90c4ebc76)
 Call ID: f44dd8f2-bf14-4c44-b98d-8ce90c4ebc76
  Args:
    source: :Alexandrine_of_Mecklenburg-Schwerin
    type: :Person
  AddTriple (1f83b5fc-bc26-4aab-bfc1-11febf364b83)
 Call ID: 1f83b5fc-bc26-4aab-bfc1-11febf364b83
  Args:
    source: :Frederik_IX
    target: :Christian_X
    relation: :hasFather
  AddTriple (e67e3d49-d86f-41d2-b390-aada8bdb5ddd)
 Call ID: e67e3d49-d86f-41d2-b390-aada8bdb5ddd
  Args:
    source: :Frederik_IX
    relation: :hasMother
    target: :Alexandrine_of_Mecklenburg-Schwerin
  AssignClass (53673735-a3fe-42e2-a459-44a878ef33e5)
 Call ID: 53673735-a3fe-42e2-a459-44a878ef33e5
  Args:
    source: :Ingrid_of_Sweden
    type: :Woman
  AssignClass (7e2d1e7f-d031-45c5-bb2d-a2d84f2db404)
 Call ID: 7e2d1e7f-d031-45c5-bb2d-a2d84f2db404
  Args:
    type: :Person
    source: :Ingrid_of_Sweden
  AddTriple (298d6e38-a63f-460f-9d5d-1a29418fdc64)
 Call ID: 298d6e38-a63f-460f-9d5d-1a29418fdc64
  Args:
    source: :Frederik_IX
    relation: :hasRelation
    target: :Ingrid_of_Sweden
  AddLiteral (2cf6fbfe-804e-43af-9362-f789f251ec02)
 Call ID: 2cf6fbfe-804e-43af-9362-f789f251ec02
  Args:
    literal_value: 1935
    relation: :hasMarriageYear
    source: :Frederik_IX
    literal_type: xsd:positiveInteger
  AssignClass (876b7505-0e51-475c-95ca-116f18921111)
 Call ID: 876b7505-0e51-475c-95ca-116f18921111
  Args:
    type: :Man
    source: :Knud
  AssignClass (51c2022b-76d2-4d1f-a2da-b4ec5b16b7a3)
 Call ID: 51c2022b-76d2-4d1f-a2da-b4ec5b16b7a3
  Args:
    type: :Person
    source: :Knud
  AddTriple (269861cc-c40f-432b-927a-6079b0ff8595)
 Call ID: 269861cc-c40f-432b-927a-6079b0ff8595
  Args:
    relation: :isSiblingOf
    target: :Knud
    source: :Frederik_IX
  AssignClass (b7cc967b-b12f-4ca5-b567-49cbc826a13d)
 Call ID: b7cc967b-b12f-4ca5-b567-49cbc826a13d
  Args:
    type: :Woman
    source: :Margrethe_II
  AssignClass (df814394-6e67-4cb2-bc00-2182927c73fc)
 Call ID: df814394-6e67-4cb2-bc00-2182927c73fc
  Args:
    type: :Person
    source: :Margrethe_II
  AddTriple (645147ab-9a87-4308-bd2f-bef5eea78663)
 Call ID: 645147ab-9a87-4308-bd2f-bef5eea78663
  Args:
    target: :Frederik_IX
    relation: :isDaughterOf
    source: :Margrethe_II
  AssignClass (bc5164c3-618a-4d3b-bac9-e4e92bdee97f)
 Call ID: bc5164c3-618a-4d3b-bac9-e4e92bdee97f
  Args:
    source: :Christian_IX
    type: :Man
  AssignClass (d8f67504-006e-4753-913e-ec4ff6f5d880)
 Call ID: d8f67504-006e-4753-913e-ec4ff6f5d880
  Args:
    type: :Person
    source: :Christian_IX
  AddTriple (95da2e20-df8f-4b59-b6fa-c12c53784173)
 Call ID: 95da2e20-df8f-4b59-b6fa-c12c53784173
  Args:
    relation: :hasAncestor
    target: :Christian_IX
    source: :Frederik_IX
  AssignClass (1b8a82d8-d849-4c75-b2b3-d49daeaf5d31)
 Call ID: 1b8a82d8-d849-4c75-b2b3-d49daeaf5d31
  Args:
    type: :Man
    source: :Frederik_VIII
  AssignClass (441aacb9-9de4-47cd-977c-4b14e6be3c4e)
 Call ID: 441aacb9-9de4-47cd-977c-4b14e6be3c4e
  Args:
    source: :Frederik_VIII
    type: :Person
  AssignClass (3c6d0120-daa3-471f-859e-90191503a58d)
 Call ID: 3c6d0120-daa3-471f-859e-90191503a58d
  Args:
    source: :Louise_of_Sweden
    type: :Woman
  AssignClass (88f66eeb-47f4-4e9c-9dae-094799c12271)
 Call ID: 88f66eeb-47f4-4e9c-9dae-094799c12271
  Args:
    source: :Louise_of_Sweden
    type: :Person
  AddTriple (efac0f28-26a6-4f32-88c6-4e2ccb671864)
 Call ID: efac0f28-26a6-4f32-88c6-4e2ccb671864
  Args:
    source: :Christian_X
    target: :Frederik_VIII
    relation: :hasFather
  AddTriple (480fb871-e444-443f-8c0c-748eb56c8175)
 Call ID: 480fb871-e444-443f-8c0c-748eb56c8175
  Args:
    source: :Christian_X
    target: :Louise_of_Sweden
    relation: :hasMother
  AssignClass (24b4234c-668c-405f-9557-a8c5f9042062)
 Call ID: 24b4234c-668c-405f-9557-a8c5f9042062
  Args:
    source: :Frederick_Francis_III
    type: :Man
  AssignClass (7e11237d-83fb-49c7-999a-970ad547650d)
 Call ID: 7e11237d-83fb-49c7-999a-970ad547650d
  Args:
    type: :Person
    source: :Frederick_Francis_III
  AssignClass (b22e2a7c-feab-4458-88da-ff405294ec9f)
 Call ID: b22e2a7c-feab-4458-88da-ff405294ec9f
  Args:
    source: :Anastasia_Mikhailovna_of_Russia
    type: :Woman
  AssignClass (de4757f2-e41e-42d1-b6a8-9cdc5655e115)
 Call ID: de4757f2-e41e-42d1-b6a8-9cdc5655e115
  Args:
    type: :Person
    source: :Anastasia_Mikhailovna_of_Russia
  AddTriple (b6acdd6c-77a9-4e67-ad6a-743bd820cdcd)
 Call ID: b6acdd6c-77a9-4e67-ad6a-743bd820cdcd
  Args:
    target: :Frederick_Francis_III
    relation: :hasFather
    source: :Alexandrine_of_Mecklenburg-Schwerin
  AddTriple (eddfad9b-23bf-495b-a15c-a47bb6825146)
 Call ID: eddfad9b-23bf-495b-a15c-a47bb6825146
  Args:
    source: :Alexandrine_of_Mecklenburg-Schwerin
    relation: :hasMother
    target: :Anastasia_Mikhailovna_of_Russia
  AssignClass (e047b72c-a632-4ae8-aa5a-771bae9e0a43)
 Call ID: e047b72c-a632-4ae8-aa5a-771bae9e0a43
  Args:
    type: :Man
    source: :Gustaf_VI_Adolf_of_Sweden
  AssignClass (49848b87-bed1-4684-9a86-9fd74d032feb)
 Call ID: 49848b87-bed1-4684-9a86-9fd74d032feb
  Args:
    type: :Person
    source: :Gustaf_VI_Adolf_of_Sweden
  AssignClass (f2d1817a-27bd-48c3-9b26-4ef3968ce978)
 Call ID: f2d1817a-27bd-48c3-9b26-4ef3968ce978
  Args:
    type: :Woman
    source: :Margaret_of_Connaught
  AssignClass (7b890f95-7144-4aed-ab44-a084d352bc78)
 Call ID: 7b890f95-7144-4aed-ab44-a084d352bc78
  Args:
    type: :Person
    source: :Margaret_of_Connaught
  AddTriple (135c8264-40bc-4961-8540-0518f713534f)
 Call ID: 135c8264-40bc-4961-8540-0518f713534f
  Args:
    target: :Gustaf_VI_Adolf_of_Sweden
    relation: :hasFather
    source: :Ingrid_of_Sweden
  AddTriple (58a74d6b-81e1-4115-9b47-f997220b9400)
 Call ID: 58a74d6b-81e1-4115-9b47-f997220b9400
  Args:
    relation: :hasMother
    target: :Margaret_of_Connaught
    source: :Ingrid_of_Sweden
  Finish (4c6a8ad2-f2df-4f98-87e2-101bebfc2245)
 Call ID: 4c6a8ad2-f2df-4f98-87e2-101bebfc2245
  Args: