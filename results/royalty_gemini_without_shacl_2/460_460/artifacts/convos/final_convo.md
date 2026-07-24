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
Donatus, Prince and Landgrave of Hesse (legally Heinrich Donatus Philipp Umberto Prinz und Landgraf von Hessen; born 17 October 1966) is a German businessman and the head of the House of Brabant and the House of Hesse.
He is the eldest son and successor of German aristocrat Moritz, Landgrave of Hesse, and his former wife, Princess Tatiana of Sayn-Wittgenstein-Berleburg (b. 1940).
Donatus's father became the head of the Hesse-Cassel line on the death of his own father, Landgrave Philipp in 1980.
Having also been the adopted son and heir of his distant cousin, Louis, Prince of Hesse and by Rhine, the latter's death in 1968 as the last male of the Hesse-Darmstadt branch left Moritz head of the entire House of Hesse, to which Donatus succeeded.
Profession

Donatus directs the Hessische Hausstiftung (Foundation of the House of Hesse), a foundation (see below) established to curate and showcase the cultural heritage and history of the House of Hesse, a dynasty which ruled the Electorate of Hesse-Cassel until 1866, the Grand Duchy of Hesse and by Rhine until 1918, and whose male-line antecedents and co-lateral ties include the Protestant leader Philip the Magnanimous, the Swedish king Frederick I, Russia's last tsarina Alexandra Feodorovna, the exiled Spanish queen Victoria Eugenie of Battenberg, and Britain's last viceroy of India, the assassinated Louis, Earl Mountbatten of Burma.
Donatus also manages Prinz von Hessen, a winery specializing in production of varietal vintages on his 45 hectare vineyard.
Marriage and issue

Donatus married the daughter of German industrial heir and Chinese honorary citizen Count Hubertus von Faber-Castell, Countess Floria Franziska Marie-Luisa Erika von Faber-Castell (born 14 October 1974, Düsseldorf), in a civil ceremony in Wiesbaden on 25 April 2003.
Prince Donatus and Floria Franziska are 6th cousins, as both descended from Frederick II, Landgrave of Hesse-Kassel and his first wife Princess Mary of Great Britain.
Held at the Johanneskirche and followed by a grand ball in the Green Salon, state room of the former Friedrichshof palace in Kronberg (now a luxury hotel and golf course owned by the House of Hesse's family foundation) where Donatus's ancestress, the German Empress Frederick, Princess Royal, lived in widowhood, more than 300 guests were present.
Among them were Caroline, Princess of Hanover, Princess Benedikte of Denmark, and Gloria, Princess of Thurn and Taxis.
Representative appearances

In 2021, Donatus was one of only 30 mourners at Prince Philip, the Duke of Edinburgh's, funeral at St George's Chapel, Windsor Castle.
King Charles III appointed Donatus his personal representative to the funeral of his first cousin Maximilian, Margrave of Baden, on 13 January 2023.
Although, as a descendant of Queen Victoria, he is only a distant relative of today's British royals who are more closely related to some other princes of Hesse, descendants of Prince Philip's sister Sophie, there is a close connection to the British royal family through Donatus' adoptive grandparents, Louis, Prince of Hesse and by Rhine, and his wife Margaret Campbell Geddes, who were relatives and close friends of Queen Elizabeth II and Prince Philip, as Philip's sister Cecilie had been married to Louis' elder brother Georg Donatus, Hereditary Grand Duke of Hesse.
The late Queen, Prince Philip and Charles (then Prince of Wales) have visited Wolfsgarten on several occasions.
Ancestry

Foundation of the House of Hesse

Founded in 1928, the Foundation of the House of Hesse is the successor institution of a family trust that had been established in 1830, confiscated by the Kingdom of Prussia in 1866, and re-established after partial restitution in 1878.
The latter is mainly shown at Fasanerie Palace in Eichenzell, Hesse, a former summer palace of the Prince Abbots of Fulda that had been taken over by the Landgraves of Hesse after the secularization and mediatisation of the Prince-bishopric of Fulda in 1803.
The Landgrave and his family live in Wolfsgarten and Panker.



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
  AssignClass (75647cd7-0b52-4057-a2b5-c745578b77f4)
 Call ID: 75647cd7-0b52-4057-a2b5-c745578b77f4
  Args:
    type: :Man
    source: Donatus
  AssignClass (c5c560af-8481-42ee-87cc-f1e2fa0fbe9e)
 Call ID: c5c560af-8481-42ee-87cc-f1e2fa0fbe9e
  Args:
    type: :Person
    source: Donatus
  AddLiteral (2b4f530d-04b7-4e4a-b8f0-72b536a320bd)
 Call ID: 2b4f530d-04b7-4e4a-b8f0-72b536a320bd
  Args:
    source: Donatus
    relation: :hasBirthYear
    literal_value: 1966
    literal_type: xsd:integer
  AssignClass (667f2d3b-5c71-4583-a25b-ef97a0e78a0f)
 Call ID: 667f2d3b-5c71-4583-a25b-ef97a0e78a0f
  Args:
    type: :Man
    source: Moritz
  AssignClass (cf48447a-8436-4c33-97bb-4e60b6067813)
 Call ID: cf48447a-8436-4c33-97bb-4e60b6067813
  Args:
    type: :Person
    source: Moritz
  AddTriple (beca4700-f004-4420-95e9-8bc04c324045)
 Call ID: beca4700-f004-4420-95e9-8bc04c324045
  Args:
    target: Donatus
    source: Moritz
    relation: :isFatherOf
  AssignClass (f67ac1ea-a0fc-4699-9350-4e6fd1540efb)
 Call ID: f67ac1ea-a0fc-4699-9350-4e6fd1540efb
  Args:
    type: :Woman
    source: Tatiana
  AssignClass (c718fde9-722e-4986-a4b5-4686e5fd1b65)
 Call ID: c718fde9-722e-4986-a4b5-4686e5fd1b65
  Args:
    type: :Person
    source: Tatiana
  AddTriple (88ccb866-2e37-45ec-a87a-d87de0e8e356)
 Call ID: 88ccb866-2e37-45ec-a87a-d87de0e8e356
  Args:
    source: Tatiana
    relation: :isMotherOf
    target: Donatus
  AddLiteral (db079bc2-c3de-4141-b1d1-21de9a548686)
 Call ID: db079bc2-c3de-4141-b1d1-21de9a548686
  Args:
    literal_value: 1940
    literal_type: xsd:integer
    source: Tatiana
    relation: :hasBirthYear
  AssignClass (495c2c58-e40c-4627-8ab4-8b7994e2a152)
 Call ID: 495c2c58-e40c-4627-8ab4-8b7994e2a152
  Args:
    type: :Man
    source: Philipp
  AssignClass (2f3c0b3d-b228-42c1-9237-30e22c16bf1c)
 Call ID: 2f3c0b3d-b228-42c1-9237-30e22c16bf1c
  Args:
    type: :Person
    source: Philipp
  AddTriple (bda3eb57-2f86-4ff4-9ef7-9d23b77053c8)
 Call ID: bda3eb57-2f86-4ff4-9ef7-9d23b77053c8
  Args:
    target: Moritz
    source: Philipp
    relation: :isFatherOf
  AddLiteral (62574912-ef4f-4cfc-903e-b504455ef782)
 Call ID: 62574912-ef4f-4cfc-903e-b504455ef782
  Args:
    source: Philipp
    relation: :hasDeathYear
    literal_value: 1980
    literal_type: xsd:integer
  AssignClass (595cac61-1605-4853-9c31-06b407e7593a)
 Call ID: 595cac61-1605-4853-9c31-06b407e7593a
  Args:
    type: :Man
    source: Louis
  AssignClass (6d7bed7a-4ccd-4f5a-9f9a-db553563e86d)
 Call ID: 6d7bed7a-4ccd-4f5a-9f9a-db553563e86d
  Args:
    type: :Person
    source: Louis
  AddLiteral (995ab066-ce2b-4b3c-ac4b-9cf77f2e0c3b)
 Call ID: 995ab066-ce2b-4b3c-ac4b-9cf77f2e0c3b
  Args:
    source: Louis
    relation: :hasDeathYear
    literal_value: 1968
    literal_type: xsd:integer
  AssignClass (6ae01c37-2500-4f4e-9dbc-1927c10a66da)
 Call ID: 6ae01c37-2500-4f4e-9dbc-1927c10a66da
  Args:
    type: :Woman
    source: FloriaFranziska
  AssignClass (37b29611-7852-4680-baf3-fb23b637215d)
 Call ID: 37b29611-7852-4680-baf3-fb23b637215d
  Args:
    type: :Person
    source: FloriaFranziska
  AddLiteral (1a509516-4543-4fad-a8e8-2f926c3564db)
 Call ID: 1a509516-4543-4fad-a8e8-2f926c3564db
  Args:
    literal_value: 1974
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: FloriaFranziska
  AddTriple (df9b4010-bd8c-4a77-82d7-3547bded530a)
 Call ID: df9b4010-bd8c-4a77-82d7-3547bded530a
  Args:
    target: FloriaFranziska
    source: Donatus
    relation: :hasRelation
  AddLiteral (7812cc28-9b43-49a6-b2ab-37ba8be40eb9)
 Call ID: 7812cc28-9b43-49a6-b2ab-37ba8be40eb9
  Args:
    literal_value: 2003
    literal_type: xsd:integer
    source: Donatus
    relation: :hasMarriageYear
  AssignClass (fc775c96-d3ac-45bb-9031-27f19778b455)
 Call ID: fc775c96-d3ac-45bb-9031-27f19778b455
  Args:
    type: :Man
    source: Hubertus
  AssignClass (805fb30c-e71f-4de7-b5f0-eb6f744153b6)
 Call ID: 805fb30c-e71f-4de7-b5f0-eb6f744153b6
  Args:
    type: :Person
    source: Hubertus
  AddTriple (b84d9422-7191-4117-a780-9c48c28fd108)
 Call ID: b84d9422-7191-4117-a780-9c48c28fd108
  Args:
    target: FloriaFranziska
    source: Hubertus
    relation: :isFatherOf
  AssignClass (a158a0fb-9acd-41a0-8e1c-de9c0803f72a)
 Call ID: a158a0fb-9acd-41a0-8e1c-de9c0803f72a
  Args:
    type: :Man
    source: FrederickII
  AssignClass (813b2ef5-bfe2-47c2-8539-2ff866d72d67)
 Call ID: 813b2ef5-bfe2-47c2-8539-2ff866d72d67
  Args:
    type: :Person
    source: FrederickII
  AssignClass (8a4d1764-4046-493d-9ffd-23b6cac67690)
 Call ID: 8a4d1764-4046-493d-9ffd-23b6cac67690
  Args:
    type: :Woman
    source: Mary
  AssignClass (a217b6f2-d0dc-4569-b92f-7067e3f6267c)
 Call ID: a217b6f2-d0dc-4569-b92f-7067e3f6267c
  Args:
    type: :Person
    source: Mary
  AddTriple (6e536221-c16d-4a5c-bec1-0f673bae3a94)
 Call ID: 6e536221-c16d-4a5c-bec1-0f673bae3a94
  Args:
    relation: :isFatherOf
    source: FrederickII
    target: Donatus
  AddTriple (82c78dea-5c6e-4c56-a355-1d298e3601cd)
 Call ID: 82c78dea-5c6e-4c56-a355-1d298e3601cd
  Args:
    relation: :isMotherOf
    source: Mary
    target: Donatus
  AddTriple (eb1bea61-3758-46b1-b646-207c1cc9bdd4)
 Call ID: eb1bea61-3758-46b1-b646-207c1cc9bdd4
  Args:
    target: FloriaFranziska
    source: FrederickII
    relation: :isFatherOf
  AddTriple (d1e01056-b32a-48f4-80db-da8a5cac2ac6)
 Call ID: d1e01056-b32a-48f4-80db-da8a5cac2ac6
  Args:
    target: FloriaFranziska
    source: Mary
    relation: :isMotherOf
  Finish (b50b34d5-a8c8-4ee7-9caf-9a6b867145ae)
 Call ID: b50b34d5-a8c8-4ee7-9caf-9a6b867145ae
  Args: