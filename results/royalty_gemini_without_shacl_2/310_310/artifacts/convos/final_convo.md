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
Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Prince Maurits Willem Pieter Hendrik of Orange-Nassau, van Vollenhoven (born 17 April 1968) is a member of the Dutch royal family as the eldest son of Princess Margriet of the Netherlands and Pieter van Vollenhoven.
Life and career

Maurits was born on 17 April 1968.
His godparents are Princess Christina of the Netherlands, Prince Alois-Konstantin of Lowenstein-Wertheim-Rosenberg, Jhr. G. Krayenhof, and The Dutch Merchant Fleet.
Van Vollenhoven has three brothers: Bernhard, Pieter-Christiaan, Floris.
In 1987, van Vollenhoven performed military service with the Royal Netherlands Marine Corps and the Royal Netherlands Navy.
From September 2001 to May 2006, the prince worked for Philips (Domestic Appliances and Personal Care) in Amersfoort, where he was in charge of part of the Philishave portfolio.
In May 2006, van Vollenhoven started his own business, The Source, which focuses on innovative concepts for products, services and systems for both business and government.
Since 1 May 2013, Maurits is Aide-de-camp to King Willem-Alexander and promoted to the rank of Commander (Dutch: Kapitein-lieutenant ter Zee) in the Royal Netherlands Navy.
Maurits works for Sunrock, a company which invests in solar parks and green energy.
The prince criticised the solar energy policy of the municipality of Amsterdam and opened up about other topics.
Marriage and family

In 1989, van Vollenhoven met Marilène (Marie-Helène) van den Broek b. 4 February 1970, the youngest daughter of Hans van den Broek and Josee van Schendel.
He was the first grandchild of Queen Juliana and Prince Bernhard of the Netherlands who married.
Together, the couple has three children:


By Royal Decree of 26 May 1998, the children of van Vollenhoven bear the surname "van Lippe-Biesterfeld van Vollenhoven", without titles.
Upon the abdication of Queen Beatrix, which took place on 30 April 2013, it was confirmed that the children of Princess Margriet and Pieter van Vollenhoven would no longer be eligible to succeed to the throne, and that they would also cease to be members of the Royal House according to The Membership of the Royal House Act.
Titles and styles

Ancestry

References

External links

2 gave up the title "Prince of the Netherlands, but still held the title "Prince of Orange-Nassau"
3 title granted by Royal Decree to descendants of Princess Irene



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
  AssignClass (b1115e90-4d8b-4c44-9283-6876e469a056)
 Call ID: b1115e90-4d8b-4c44-9283-6876e469a056
  Args:
    type: :Woman
    source: Princess_Beatrix
  AssignClass (b82dcc45-81a5-4b24-9abf-b58331f1ad8d)
 Call ID: b82dcc45-81a5-4b24-9abf-b58331f1ad8d
  Args:
    type: :Woman
    source: Princess_Margriet
  AssignClass (b9c34208-2a56-4b56-b2ab-d348d4110843)
 Call ID: b9c34208-2a56-4b56-b2ab-d348d4110843
  Args:
    type: :Man
    source: Pieter_van_Vollenhoven
  AssignClass (ad2740b6-5cc7-4adf-803c-7b7f61c0445e)
 Call ID: ad2740b6-5cc7-4adf-803c-7b7f61c0445e
  Args:
    type: :Man
    source: Prince_Maurits_van_Vollenhoven
  AddLiteral (6dd67f04-7099-41c8-896a-6e59c845f0b5)
 Call ID: 6dd67f04-7099-41c8-896a-6e59c845f0b5
  Args:
    literal_type: xsd:integer
    literal_value: 1968
    relation: :hasBirthYear
    source: Prince_Maurits_van_Vollenhoven
  AddTriple (bf681b70-152a-478f-bc1f-231c899d16a1)
 Call ID: bf681b70-152a-478f-bc1f-231c899d16a1
  Args:
    relation: :hasMother
    source: Prince_Maurits_van_Vollenhoven
    target: Princess_Margriet
  AddTriple (5afdb9ca-7f12-4648-8ba1-845a20879561)
 Call ID: 5afdb9ca-7f12-4648-8ba1-845a20879561
  Args:
    relation: :hasFather
    source: Prince_Maurits_van_Vollenhoven
    target: Pieter_van_Vollenhoven
  AssignClass (5428a7f0-0029-4149-936c-42849a98c101)
 Call ID: 5428a7f0-0029-4149-936c-42849a98c101
  Args:
    type: :Man
    source: Bernhard_van_Vollenhoven
  AssignClass (478fab93-2302-48c0-b262-cdc2cc57f3c7)
 Call ID: 478fab93-2302-48c0-b262-cdc2cc57f3c7
  Args:
    type: :Man
    source: Pieter_Christiaan_van_Vollenhoven
  AssignClass (df7d5501-d34c-41e0-b600-94ab2fee961e)
 Call ID: df7d5501-d34c-41e0-b600-94ab2fee961e
  Args:
    type: :Man
    source: Floris_van_Vollenhoven
  AddTriple (a24add49-ac5c-4ff9-bebe-11aa60264093)
 Call ID: a24add49-ac5c-4ff9-bebe-11aa60264093
  Args:
    target: Bernhard_van_Vollenhoven
    source: Prince_Maurits_van_Vollenhoven
    relation: :isSiblingOf
  AddTriple (32ea9a16-c0e5-434b-b058-155da15f5eee)
 Call ID: 32ea9a16-c0e5-434b-b058-155da15f5eee
  Args:
    target: Pieter_Christiaan_van_Vollenhoven
    relation: :isSiblingOf
    source: Prince_Maurits_van_Vollenhoven
  AddTriple (8b71371a-7ec0-4d51-a8d7-e2315f876b11)
 Call ID: 8b71371a-7ec0-4d51-a8d7-e2315f876b11
  Args:
    relation: :isSiblingOf
    source: Prince_Maurits_van_Vollenhoven
    target: Floris_van_Vollenhoven
  AssignClass (94e98b7a-00e9-4657-ae3e-4ba3ad093669)
 Call ID: 94e98b7a-00e9-4657-ae3e-4ba3ad093669
  Args:
    type: :Woman
    source: Marilene_van_den_Broek
  AddLiteral (a05e8712-79c5-4ece-9ad9-c8a90d41d010)
 Call ID: a05e8712-79c5-4ece-9ad9-c8a90d41d010
  Args:
    literal_type: xsd:integer
    literal_value: 1970
    relation: :hasBirthYear
    source: Marilene_van_den_Broek
  AddLiteral (8f874cc7-6707-49aa-aec6-b790a1971f11)
 Call ID: 8f874cc7-6707-49aa-aec6-b790a1971f11
  Args:
    relation: :hasMarriageYear
    source: Prince_Maurits_van_Vollenhoven
    literal_value: 1989
    literal_type: xsd:integer
  AddTriple (f17d93e5-091c-4a8f-8bd1-0632f9cc8df5)
 Call ID: f17d93e5-091c-4a8f-8bd1-0632f9cc8df5
  Args:
    target: Marilene_van_den_Broek
    relation: :hasRelation
    source: Prince_Maurits_van_Vollenhoven
  AssignClass (1f771577-a481-4954-b6bc-610ef1eaef6e)
 Call ID: 1f771577-a481-4954-b6bc-610ef1eaef6e
  Args:
    type: :Man
    source: Hans_van_den_Broek
  AssignClass (bfb3507c-2e4e-40c5-ad4f-5c32e3ea6846)
 Call ID: bfb3507c-2e4e-40c5-ad4f-5c32e3ea6846
  Args:
    type: :Woman
    source: Josee_van_Schendel
  AddTriple (c29b144e-25c4-4609-9ed4-4854d2f843bd)
 Call ID: c29b144e-25c4-4609-9ed4-4854d2f843bd
  Args:
    source: Marilene_van_den_Broek
    relation: :hasFather
    target: Hans_van_den_Broek
  AddTriple (95d61daa-b2b4-4adb-99bf-74ad806992f8)
 Call ID: 95d61daa-b2b4-4adb-99bf-74ad806992f8
  Args:
    relation: :hasMother
    source: Marilene_van_den_Broek
    target: Josee_van_Schendel
  AssignClass (14e81470-1b64-42f0-81db-33af09ec0d3e)
 Call ID: 14e81470-1b64-42f0-81db-33af09ec0d3e
  Args:
    type: :Woman
    source: Queen_Juliana
  AssignClass (a0612e9c-08ef-4a0a-a854-10bf482bdc30)
 Call ID: a0612e9c-08ef-4a0a-a854-10bf482bdc30
  Args:
    type: :Man
    source: Prince_Bernhard_of_the_Netherlands
  AddTriple (bae71a9d-8642-4833-8329-bc846a947a49)
 Call ID: bae71a9d-8642-4833-8329-bc846a947a49
  Args:
    source: Princess_Margriet
    relation: :hasFather
    target: Prince_Bernhard_of_the_Netherlands
  AddTriple (bfac1590-0fa3-4b61-a944-31053701ff6b)
 Call ID: bfac1590-0fa3-4b61-a944-31053701ff6b
  Args:
    target: Queen_Juliana
    relation: :hasMother
    source: Princess_Margriet
  Finish (305cde6a-e3ce-452c-b587-e4cfc28c339c)
 Call ID: 305cde6a-e3ce-452c-b587-e4cfc28c339c
  Args: