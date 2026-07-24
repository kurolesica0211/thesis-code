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
  AssignClass (8911ca42-24d5-4850-9010-20b34d731c92)
 Call ID: 8911ca42-24d5-4850-9010-20b34d731c92
  Args:
    type: :Man
    source: Frederik_IX
  AssignClass (739c3698-a06e-4223-9e08-39fcd74b7370)
 Call ID: 739c3698-a06e-4223-9e08-39fcd74b7370
  Args:
    source: Frederik_IX
    type: :Person
  AddLiteral (30d024c0-771b-415a-840c-18867799884d)
 Call ID: 30d024c0-771b-415a-840c-18867799884d
  Args:
    source: Frederik_IX
    relation: :knownAs
    literal_value: Christian Frederik Franz Michael Carl Valdemar Georg
    literal_type: xsd:string
  AddLiteral (5128908a-d965-4459-94a4-d74fd45a6cf8)
 Call ID: 5128908a-d965-4459-94a4-d74fd45a6cf8
  Args:
    literal_type: xsd:positiveInteger
    literal_value: 1899
    relation: :hasBirthYear
    source: Frederik_IX
  AddLiteral (921cd0ab-a7da-493b-ac8f-22954c5b168d)
 Call ID: 921cd0ab-a7da-493b-ac8f-22954c5b168d
  Args:
    literal_type: xsd:positiveInteger
    literal_value: 1972
    relation: :hasDeathYear
    source: Frederik_IX
  AssignClass (360ce40b-12ad-419a-a204-6bdbff4b2b30)
 Call ID: 360ce40b-12ad-419a-a204-6bdbff4b2b30
  Args:
    source: Christian_X
    type: :Man
  AssignClass (4923d80c-6c12-4a83-a26b-2b1c06525013)
 Call ID: 4923d80c-6c12-4a83-a26b-2b1c06525013
  Args:
    type: :Person
    source: Christian_X
  AssignClass (49851aa5-5054-4f15-8b38-15db5835e7ae)
 Call ID: 49851aa5-5054-4f15-8b38-15db5835e7ae
  Args:
    type: :Woman
    source: Alexandrine_of_Mecklenburg-Schwerin
  AssignClass (3a672560-027e-467e-b623-ddd00703c702)
 Call ID: 3a672560-027e-467e-b623-ddd00703c702
  Args:
    type: :Person
    source: Alexandrine_of_Mecklenburg-Schwerin
  AddTriple (c5b2d454-8071-42b4-a5c0-6e38a923f89c)
 Call ID: c5b2d454-8071-42b4-a5c0-6e38a923f89c
  Args:
    target: Christian_X
    source: Frederik_IX
    relation: :hasFather
  AddTriple (a426a39e-287c-41ff-ab6f-4b74677f14f6)
 Call ID: a426a39e-287c-41ff-ab6f-4b74677f14f6
  Args:
    relation: :hasMother
    source: Frederik_IX
    target: Alexandrine_of_Mecklenburg-Schwerin
  AssignClass (67e0bb56-5e90-4f6e-aff2-21402c24861a)
 Call ID: 67e0bb56-5e90-4f6e-aff2-21402c24861a
  Args:
    type: :Woman
    source: Ingrid_of_Sweden
  AssignClass (16674067-f832-4830-989a-4bbf54264144)
 Call ID: 16674067-f832-4830-989a-4bbf54264144
  Args:
    type: :Person
    source: Ingrid_of_Sweden
  AddTriple (7d830f2d-f922-45a0-ae34-1321854236ee)
 Call ID: 7d830f2d-f922-45a0-ae34-1321854236ee
  Args:
    relation: :hasRelation
    source: Frederik_IX
    target: Ingrid_of_Sweden
  AddLiteral (7cf62d5e-5fbe-4dce-972e-4c2e85e2f202)
 Call ID: 7cf62d5e-5fbe-4dce-972e-4c2e85e2f202
  Args:
    relation: :hasMarriageYear
    source: Frederik_IX
    literal_type: xsd:positiveInteger
    literal_value: 1935
  AssignClass (ee42fdea-e787-46a3-8691-eb8ca18e11ba)
 Call ID: ee42fdea-e787-46a3-8691-eb8ca18e11ba
  Args:
    source: Knud
    type: :Man
  AssignClass (d15ade95-ed07-4b42-ad63-c0ffd800e6e0)
 Call ID: d15ade95-ed07-4b42-ad63-c0ffd800e6e0
  Args:
    source: Knud
    type: :Person
  AddTriple (3449c937-e46b-4233-bcd9-353bfe75c2bc)
 Call ID: 3449c937-e46b-4233-bcd9-353bfe75c2bc
  Args:
    relation: :isSiblingOf
    source: Frederik_IX
    target: Knud
  AssignClass (ef438f7a-7217-4839-9b90-8dbd4100b2d9)
 Call ID: ef438f7a-7217-4839-9b90-8dbd4100b2d9
  Args:
    source: Margrethe_II
    type: :Woman
  AssignClass (77e05a8e-bb31-4b4f-849e-8052deccdea6)
 Call ID: 77e05a8e-bb31-4b4f-849e-8052deccdea6
  Args:
    type: :Person
    source: Margrethe_II
  AddTriple (823ad491-4f19-45fa-8234-ce729d0bd284)
 Call ID: 823ad491-4f19-45fa-8234-ce729d0bd284
  Args:
    target: Frederik_IX
    source: Margrethe_II
    relation: :isDaughterOf
  AssignClass (bc743f80-db59-4263-bfbb-b4f0d6ca7ee3)
 Call ID: bc743f80-db59-4263-bfbb-b4f0d6ca7ee3
  Args:
    source: Christian_IX
    type: :Man
  AssignClass (6edabf99-10b4-4d6d-a385-0e28215b1097)
 Call ID: 6edabf99-10b4-4d6d-a385-0e28215b1097
  Args:
    type: :Person
    source: Christian_IX
  AssignClass (157eedb6-fb86-4119-bc9d-75c38bf0f3fa)
 Call ID: 157eedb6-fb86-4119-bc9d-75c38bf0f3fa
  Args:
    source: Frederik_VIII
    type: :Man
  AssignClass (7f631cbe-2de5-4126-a42c-a77653acff35)
 Call ID: 7f631cbe-2de5-4126-a42c-a77653acff35
  Args:
    source: Frederik_VIII
    type: :Person
  AssignClass (c341379e-1ac0-4f20-90b3-401dedb7c8c7)
 Call ID: c341379e-1ac0-4f20-90b3-401dedb7c8c7
  Args:
    source: Louise_of_Sweden
    type: :Woman
  AssignClass (d375520f-f8a5-4d8f-a02d-18c9a581cff5)
 Call ID: d375520f-f8a5-4d8f-a02d-18c9a581cff5
  Args:
    type: :Person
    source: Louise_of_Sweden
  AddTriple (d4543d00-cbe6-426a-8b57-59e8bc2974cf)
 Call ID: d4543d00-cbe6-426a-8b57-59e8bc2974cf
  Args:
    relation: :hasFather
    source: Christian_X
    target: Frederik_VIII
  AddTriple (4fa82540-2139-43c2-b633-f663f8f576cb)
 Call ID: 4fa82540-2139-43c2-b633-f663f8f576cb
  Args:
    relation: :hasMother
    source: Christian_X
    target: Louise_of_Sweden
  AssignClass (be1f444a-0436-4ffb-aa0f-e6eb06ee6f52)
 Call ID: be1f444a-0436-4ffb-aa0f-e6eb06ee6f52
  Args:
    source: Frederick_Francis_III
    type: :Man
  AssignClass (268d75e5-054b-4df4-a12f-dc039ce970b5)
 Call ID: 268d75e5-054b-4df4-a12f-dc039ce970b5
  Args:
    source: Frederick_Francis_III
    type: :Person
  AssignClass (fc9a551d-e96b-434d-80b9-b505d55256aa)
 Call ID: fc9a551d-e96b-434d-80b9-b505d55256aa
  Args:
    type: :Woman
    source: Anastasia_Mikhailovna_of_Russia
  AssignClass (50a2a30c-947f-4075-95f0-12197e22d7a8)
 Call ID: 50a2a30c-947f-4075-95f0-12197e22d7a8
  Args:
    source: Anastasia_Mikhailovna_of_Russia
    type: :Person
  AddTriple (8c6501e0-40cc-42f2-9a45-2be461463c4d)
 Call ID: 8c6501e0-40cc-42f2-9a45-2be461463c4d
  Args:
    relation: :hasFather
    source: Alexandrine_of_Mecklenburg-Schwerin
    target: Frederick_Francis_III
  AddTriple (b698b7e1-956b-42e2-b178-1191f6e58882)
 Call ID: b698b7e1-956b-42e2-b178-1191f6e58882
  Args:
    source: Alexandrine_of_Mecklenburg-Schwerin
    relation: :hasMother
    target: Anastasia_Mikhailovna_of_Russia
  AssignClass (566fc6e7-1c65-478c-90ad-993311d7c1a9)
 Call ID: 566fc6e7-1c65-478c-90ad-993311d7c1a9
  Args:
    source: Gustaf_VI_Adolf
    type: :Man
  AssignClass (c9450838-ab35-414b-acca-c089da1b1bda)
 Call ID: c9450838-ab35-414b-acca-c089da1b1bda
  Args:
    source: Gustaf_VI_Adolf
    type: :Person
  AssignClass (357d72c5-a76e-4f4e-9007-43908dedd037)
 Call ID: 357d72c5-a76e-4f4e-9007-43908dedd037
  Args:
    type: :Woman
    source: Margaret_of_Connaught
  AssignClass (e1ea784c-4189-465f-b264-db8a99e25ee8)
 Call ID: e1ea784c-4189-465f-b264-db8a99e25ee8
  Args:
    type: :Person
    source: Margaret_of_Connaught
  AddTriple (cbb05ff9-ee25-4489-b83e-407fc9857af3)
 Call ID: cbb05ff9-ee25-4489-b83e-407fc9857af3
  Args:
    relation: :hasFather
    source: Ingrid_of_Sweden
    target: Gustaf_VI_Adolf
  AddTriple (b54b54bb-2f13-4eed-a85d-574db8bca9bb)
 Call ID: b54b54bb-2f13-4eed-a85d-574db8bca9bb
  Args:
    source: Ingrid_of_Sweden
    relation: :hasMother
    target: Margaret_of_Connaught
  Finish (5724eb1b-e637-43c0-b246-4914226f7b21)
 Call ID: 5724eb1b-e637-43c0-b246-4914226f7b21
  Args: