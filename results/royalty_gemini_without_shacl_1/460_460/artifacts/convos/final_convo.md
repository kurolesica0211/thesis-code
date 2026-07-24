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
  AssignClass (fa37b856-d536-44f0-ad57-5e39e04ce5ee)
 Call ID: fa37b856-d536-44f0-ad57-5e39e04ce5ee
  Args:
    type: :Man
    source: Donatus
  AssignClass (fb34ab1c-6acf-42a7-8280-d83787292b32)
 Call ID: fb34ab1c-6acf-42a7-8280-d83787292b32
  Args:
    source: Moritz
    type: :Man
  AssignClass (5b693aa1-c44f-4d65-b16e-2f5ce58e9a43)
 Call ID: 5b693aa1-c44f-4d65-b16e-2f5ce58e9a43
  Args:
    source: Tatiana
    type: :Woman
  AssignClass (df9e1e28-6a44-46a3-9afc-51ed6e1c53c9)
 Call ID: df9e1e28-6a44-46a3-9afc-51ed6e1c53c9
  Args:
    source: Philipp
    type: :Man
  AssignClass (03067461-4d70-404a-b123-43b30475e2b4)
 Call ID: 03067461-4d70-404a-b123-43b30475e2b4
  Args:
    type: :Woman
    source: Floria_Franziska
  AssignClass (fc78e8ed-7514-4e8d-bb5d-fc41653d78bb)
 Call ID: fc78e8ed-7514-4e8d-bb5d-fc41653d78bb
  Args:
    source: Hubertus_von_Faber-Castell
    type: :Man
  AddLiteral (668da1b4-e082-41a6-b443-dc8085763ea5)
 Call ID: 668da1b4-e082-41a6-b443-dc8085763ea5
  Args:
    source: Donatus
    literal_value: 1966
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (66b8ba15-a33b-462f-942b-dd754cd0e763)
 Call ID: 66b8ba15-a33b-462f-942b-dd754cd0e763
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1940
    source: Tatiana
  AddLiteral (1ae83f23-f355-4d84-8a03-83e5e0b36b60)
 Call ID: 1ae83f23-f355-4d84-8a03-83e5e0b36b60
  Args:
    source: Floria_Franziska
    literal_value: 1974
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (624c9188-9c75-4867-b666-955bcee81714)
 Call ID: 624c9188-9c75-4867-b666-955bcee81714
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1980
    source: Philipp
  AddLiteral (f7fd1389-3ae1-45c5-8d86-cff8e4251bcc)
 Call ID: f7fd1389-3ae1-45c5-8d86-cff8e4251bcc
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 2003
    source: Donatus
  AddTriple (98214ef2-78d6-40bd-acaa-26139b6b5ab3)
 Call ID: 98214ef2-78d6-40bd-acaa-26139b6b5ab3
  Args:
    source: Donatus
    relation: :hasFather
    target: Moritz
  AddTriple (ad230e95-e08c-43b8-b0c6-ee13283d2f5b)
 Call ID: ad230e95-e08c-43b8-b0c6-ee13283d2f5b
  Args:
    source: Donatus
    target: Tatiana
    relation: :hasMother
  AddTriple (17571e07-c3af-40dd-9148-28a67357b63e)
 Call ID: 17571e07-c3af-40dd-9148-28a67357b63e
  Args:
    target: Philipp
    relation: :hasFather
    source: Moritz
  AddTriple (670c1079-68b5-48e4-8b36-9607392327ef)
 Call ID: 670c1079-68b5-48e4-8b36-9607392327ef
  Args:
    relation: :hasFather
    target: Hubertus_von_Faber-Castell
    source: Floria_Franziska
  AddTriple (041fd09f-9977-459e-8a3b-6c03ec70b2e7)
 Call ID: 041fd09f-9977-459e-8a3b-6c03ec70b2e7
  Args:
    source: Donatus
    relation: :hasFather
    target: Floria_Franziska
  Finish (40387791-b426-48a9-82c5-40a57b7e1972)
 Call ID: 40387791-b426-48a9-82c5-40a57b7e1972
  Args: