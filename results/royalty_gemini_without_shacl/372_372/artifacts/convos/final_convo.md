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
Prince George William of Hanover and Cumberland (Georg Wilhelm Ernst August Friedrich Axel Prinz von Hannover; 25 March 1915 – 8 January 2006) was the second-eldest son of Ernest Augustus, Duke of Brunswick, and his wife Princess Victoria Louise of Prussia, the only daughter of Wilhelm II, German Emperor, and Augusta Victoria of Schleswig-Holstein.
George William's wife was a sister of Prince Philip, Duke of Edinburgh, and his children are thus first cousins of King Charles III.
His sister, Frederica, became Queen of the Hellenes as the consort of King Paul of Greece.
He held the title of Prince of the United Kingdom of Great Britain and Ireland, granted ad personam to the children of the then-Duke of Brunswick by George V's letters patent of 1914, which remained unrevoked.
Life

George William was christened on 10 May 1915 in Brunswick.
The prince's godparents included Maria Christina of Austria, Prince Axel of Denmark, and Princess Olga of Hanover and Cumberland who held the infant prince over the baptismal font.
From 1930 through 1934, Prince George William attended the elite boarding school Schule Schloss Salem in Überlingen on Lake Constance.
Schule Schloss Salem was co-founded by the prince's uncle, the last Chancellor of the German Empire, Prince Maximilian of Baden, and educator Kurt Hahn in 1920.
A former student of the institution, the prince then went to Scotland with his wife to meet with Kurt Hahn, the founder of the school, and to visit Gordonstoun, the establishment that the latter founded when he had to flee Nazi Germany because of his Jewish origins.
Together with his wife, as well as his three brothers, he took part in the ship tours organized by his sister Queen Frederica and her husband King Paul of Greece in 1954 and 1956, which became known as the “Cruises of the Kings” and were attended by over 100 royals from all over Europe.
For many years Prince George William was a member of the International Olympic Committee (IOC) and of the Deutscher Olympischer Sportbund (DOSB), the German NOC.
Prince George William of Hanover lived in Schliersee, near Munich, and died in Munich in 2006 aged 90.
His wife, Sophie, sister of Prince Philip of Greece and Denmark, later Duke of Edinburgh, consort of Queen Elizabeth II of the United Kingdom, died in 2001.
Marriage

On 23 April 1946 in Salem, Baden-Württemberg, Germany, Prince George William married his third cousin Princess Sophie of Greece and Denmark, daughter of Prince Andrew of Greece and Denmark and Princess Alice of Battenberg, and the widow of Prince Christoph of Hesse.
After consultations with the Foreign Office, Home Office and King George VI's private secretary, Sir Alan Lascelles, a ciphered telegram dated 18 April 1946 and crafted by Sir Albert Napier, permanent secretary to the Lord Chancellor, was transmitted from the British Foreign Office to the Foreign Adviser to the British Commander in Chief at Berlin:


"The Duke of Brunswick has formally applied to The King by letter of March 22nd for the consent of His Majesty under the Act 12 Geo.
11 to the marriage of his son Prince George William with Princess Sophia Dowager Princess of Hesse.
Please convey to the Duke an informal intimation that in view of the fact that a state of war still exists between Great Britain and Germany, His Majesty is advised that the case is not one in which it is practicable for His consent to be given in the manner contemplated by the Act.
"

They had three children: Welf (1947–1981), Georg (born 1949) and Friederike (born 1954).
Ancestry

George William was a descendant of Victoria of the United Kingdom and Albert, Prince Consort through their eldest daughter Victoria, Princess Royal, the wife of Frederick III, German Emperor.
He was born a Prince of the United Kingdom of Great Britain and Ireland.



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
  AssignClass (745c1434-6878-4a64-8dd6-710fc4b66de0)
 Call ID: 745c1434-6878-4a64-8dd6-710fc4b66de0
  Args:
    source: :GeorgeWilliamOfHanover
    type: :Man
  AssignClass (b9c505c3-6fa1-4334-bc93-ab45199ba559)
 Call ID: b9c505c3-6fa1-4334-bc93-ab45199ba559
  Args:
    source: :GeorgeWilliamOfHanover
    type: :Person
  AddLiteral (136e9d9c-3eb1-45ab-922f-1c3d5a2077fa)
 Call ID: 136e9d9c-3eb1-45ab-922f-1c3d5a2077fa
  Args:
    source: :GeorgeWilliamOfHanover
    relation: :hasBirthYear
    literal_value: 1915
    literal_type: xsd:integer
  AddLiteral (1d2d8d48-8160-422d-a858-c287cc8a41ef)
 Call ID: 1d2d8d48-8160-422d-a858-c287cc8a41ef
  Args:
    literal_type: xsd:integer
    source: :GeorgeWilliamOfHanover
    relation: :hasDeathYear
    literal_value: 2006
  AssignClass (89b212e3-2252-45ad-97a5-bb1c8a8c38e5)
 Call ID: 89b212e3-2252-45ad-97a5-bb1c8a8c38e5
  Args:
    source: :ErnestAugustusDukeOfBrunswick
    type: :Man
  AssignClass (dda691c1-caea-42c3-9624-60fa1daf7cdb)
 Call ID: dda691c1-caea-42c3-9624-60fa1daf7cdb
  Args:
    source: :ErnestAugustusDukeOfBrunswick
    type: :Person
  AssignClass (c5fc60e1-5e5a-4187-8b30-5f74351bccb0)
 Call ID: c5fc60e1-5e5a-4187-8b30-5f74351bccb0
  Args:
    source: :VictoriaLouiseOfPrussia
    type: :Woman
  AssignClass (98ae9919-a98d-440d-8eb7-3417d5969f9a)
 Call ID: 98ae9919-a98d-440d-8eb7-3417d5969f9a
  Args:
    source: :VictoriaLouiseOfPrussia
    type: :Person
  AddTriple (5346f3a3-4620-4341-bdfa-1342891ed3c6)
 Call ID: 5346f3a3-4620-4341-bdfa-1342891ed3c6
  Args:
    target: :ErnestAugustusDukeOfBrunswick
    relation: :hasFather
    source: :GeorgeWilliamOfHanover
  AddTriple (e807a4b5-781c-4714-bdc7-18fa60b4eb96)
 Call ID: e807a4b5-781c-4714-bdc7-18fa60b4eb96
  Args:
    source: :GeorgeWilliamOfHanover
    relation: :hasMother
    target: :VictoriaLouiseOfPrussia
  AssignClass (80adc319-4942-44c0-9638-7de5f617a210)
 Call ID: 80adc319-4942-44c0-9638-7de5f617a210
  Args:
    source: :WilhelmII
    type: :Man
  AssignClass (7c0b96d1-eadc-4823-a190-612bf2676c9e)
 Call ID: 7c0b96d1-eadc-4823-a190-612bf2676c9e
  Args:
    source: :WilhelmII
    type: :Person
  AssignClass (37d214bf-d939-4879-a270-aee7a9ca100d)
 Call ID: 37d214bf-d939-4879-a270-aee7a9ca100d
  Args:
    source: :AugustaVictoriaOfSchleswigHolstein
    type: :Woman
  AssignClass (81f6fcc7-7846-4d6e-9314-7f8e18d53872)
 Call ID: 81f6fcc7-7846-4d6e-9314-7f8e18d53872
  Args:
    source: :AugustaVictoriaOfSchleswigHolstein
    type: :Person
  AddTriple (246e51e9-7f35-4767-a66b-57a4d133f0cd)
 Call ID: 246e51e9-7f35-4767-a66b-57a4d133f0cd
  Args:
    target: :WilhelmII
    relation: :hasFather
    source: :VictoriaLouiseOfPrussia
  AddTriple (ee1273f1-e443-466a-8565-367fdb11aeec)
 Call ID: ee1273f1-e443-466a-8565-367fdb11aeec
  Args:
    target: :AugustaVictoriaOfSchleswigHolstein
    relation: :hasMother
    source: :VictoriaLouiseOfPrussia
  AssignClass (2cd5970d-48a1-422c-80f8-4d78ef140836)
 Call ID: 2cd5970d-48a1-422c-80f8-4d78ef140836
  Args:
    source: :FredericaOfGreece
    type: :Woman
  AssignClass (65bda678-aad4-4ad0-9911-9a0d73a5ea7b)
 Call ID: 65bda678-aad4-4ad0-9911-9a0d73a5ea7b
  Args:
    source: :FredericaOfGreece
    type: :Person
  AddTriple (855ec723-10e1-496d-b8ee-34ae761dc153)
 Call ID: 855ec723-10e1-496d-b8ee-34ae761dc153
  Args:
    source: :GeorgeWilliamOfHanover
    target: :FredericaOfGreece
    relation: :hasSister
  AssignClass (3319b1fd-fa2c-41a5-929d-d07f9fa2fa10)
 Call ID: 3319b1fd-fa2c-41a5-929d-d07f9fa2fa10
  Args:
    source: :PaulOfGreece
    type: :Man
  AssignClass (f275d239-34b3-402d-aff1-a791f756ff22)
 Call ID: f275d239-34b3-402d-aff1-a791f756ff22
  Args:
    source: :PaulOfGreece
    type: :Person
  AddTriple (db674c04-af0f-4f5b-a78b-4edb91c48fbb)
 Call ID: db674c04-af0f-4f5b-a78b-4edb91c48fbb
  Args:
    relation: :hasMother
    target: :VictoriaLouiseOfPrussia
    source: :FredericaOfGreece
  AddTriple (3f646797-1c20-476c-bfc2-60de2326a92a)
 Call ID: 3f646797-1c20-476c-bfc2-60de2326a92a
  Args:
    source: :FredericaOfGreece
    target: :ErnestAugustusDukeOfBrunswick
    relation: :hasFather
  AssignClass (edc81214-696b-48d1-a2bd-6a90adae9fd3)
 Call ID: edc81214-696b-48d1-a2bd-6a90adae9fd3
  Args:
    source: :SophieOfGreeceAndDenmark
    type: :Woman
  AssignClass (62eab072-dcf9-450a-b8e8-505e332a1e65)
 Call ID: 62eab072-dcf9-450a-b8e8-505e332a1e65
  Args:
    source: :SophieOfGreeceAndDenmark
    type: :Person
  AddTriple (0bb95481-4b6f-42cc-8613-cca42223df96)
 Call ID: 0bb95481-4b6f-42cc-8613-cca42223df96
  Args:
    source: :GeorgeWilliamOfHanover
    target: :SophieOfGreeceAndDenmark
    relation: :hasMother
  AddLiteral (b8c56d53-b62f-4a6d-839c-8fba6225b554)
 Call ID: b8c56d53-b62f-4a6d-839c-8fba6225b554
  Args:
    source: :GeorgeWilliamOfHanover
    relation: :hasMarriageYear
    literal_value: 1946
    literal_type: xsd:integer
  AddLiteral (43998121-b8b9-4a9d-8ac0-724ac1fea0bb)
 Call ID: 43998121-b8b9-4a9d-8ac0-724ac1fea0bb
  Args:
    literal_type: xsd:integer
    source: :SophieOfGreeceAndDenmark
    literal_value: 2001
    relation: :hasDeathYear
  AssignClass (5a4cab1f-abfb-40bd-8337-94c67885952d)
 Call ID: 5a4cab1f-abfb-40bd-8337-94c67885952d
  Args:
    source: :AndrewOfGreeceAndDenmark
    type: :Man
  AssignClass (2208a10d-87ce-4064-aafe-40bcd087e514)
 Call ID: 2208a10d-87ce-4064-aafe-40bcd087e514
  Args:
    source: :AndrewOfGreeceAndDenmark
    type: :Person
  AssignClass (e7d283cf-1e80-46a8-8ba7-3e68eba7ddc6)
 Call ID: e7d283cf-1e80-46a8-8ba7-3e68eba7ddc6
  Args:
    source: :AliceOfBattenberg
    type: :Woman
  AssignClass (bd2993f9-5333-484d-afa2-5f7798edf1d9)
 Call ID: bd2993f9-5333-484d-afa2-5f7798edf1d9
  Args:
    source: :AliceOfBattenberg
    type: :Person
  AddTriple (15284203-fc2a-4280-88f9-fdf7ef829f46)
 Call ID: 15284203-fc2a-4280-88f9-fdf7ef829f46
  Args:
    target: :AndrewOfGreeceAndDenmark
    relation: :hasFather
    source: :SophieOfGreeceAndDenmark
  AddTriple (40bcd848-da60-4cfa-9143-c4be89269b43)
 Call ID: 40bcd848-da60-4cfa-9143-c4be89269b43
  Args:
    source: :SophieOfGreeceAndDenmark
    relation: :hasMother
    target: :AliceOfBattenberg
  AssignClass (33ffd0aa-4185-45fe-a0da-b53b50339c51)
 Call ID: 33ffd0aa-4185-45fe-a0da-b53b50339c51
  Args:
    source: :Welf
    type: :Man
  AssignClass (5e85cf7f-41b5-45fa-a233-f250961c8b34)
 Call ID: 5e85cf7f-41b5-45fa-a233-f250961c8b34
  Args:
    source: :Welf
    type: :Person
  AssignClass (2719ead5-11c6-4626-9eac-8a4b56025cb4)
 Call ID: 2719ead5-11c6-4626-9eac-8a4b56025cb4
  Args:
    source: :Georg
    type: :Man
  AssignClass (74ae4d29-deee-4815-97b8-7c9622045670)
 Call ID: 74ae4d29-deee-4815-97b8-7c9622045670
  Args:
    source: :Georg
    type: :Person
  AssignClass (bb60b97b-744d-4b49-b82f-74962d6308db)
 Call ID: bb60b97b-744d-4b49-b82f-74962d6308db
  Args:
    source: :Friederike
    type: :Woman
  AssignClass (9c3808d4-2585-4186-a4c0-1532a1c0ec7a)
 Call ID: 9c3808d4-2585-4186-a4c0-1532a1c0ec7a
  Args:
    source: :Friederike
    type: :Person
  AddTriple (e08dc926-a3cb-42db-a4c2-39e72ab8ef14)
 Call ID: e08dc926-a3cb-42db-a4c2-39e72ab8ef14
  Args:
    source: :GeorgeWilliamOfHanover
    relation: :hasSon
    target: :Welf
  AddTriple (9a9bb34f-7006-40f4-99e5-8f33dcaf7eb2)
 Call ID: 9a9bb34f-7006-40f4-99e5-8f33dcaf7eb2
  Args:
    relation: :hasSon
    target: :Georg
    source: :GeorgeWilliamOfHanover
  AddTriple (9ecf8ecd-e766-47a1-9d72-ddfa00ae5aaa)
 Call ID: 9ecf8ecd-e766-47a1-9d72-ddfa00ae5aaa
  Args:
    source: :GeorgeWilliamOfHanover
    relation: :hasDaughter
    target: :Friederike
  AddTriple (4fff60a6-4f3b-4646-b9d5-1abd7c29a427)
 Call ID: 4fff60a6-4f3b-4646-b9d5-1abd7c29a427
  Args:
    relation: :hasMother
    target: :SophieOfGreeceAndDenmark
    source: :Welf
  AddTriple (28f4b1f5-603a-4a75-933a-814125340a75)
 Call ID: 28f4b1f5-603a-4a75-933a-814125340a75
  Args:
    source: :Georg
    relation: :hasMother
    target: :SophieOfGreeceAndDenmark
  AddTriple (9e8678ce-d858-40b3-a776-bb0dac631712)
 Call ID: 9e8678ce-d858-40b3-a776-bb0dac631712
  Args:
    relation: :hasMother
    target: :SophieOfGreeceAndDenmark
    source: :Friederike
  Finish (7bb533db-43a6-4a6d-acb7-6d1b66cc2e18)
 Call ID: 7bb533db-43a6-4a6d-acb7-6d1b66cc2e18
  Args: