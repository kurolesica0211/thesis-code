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
Princess Irene of Greece and Denmark, Duchess of Aosta (Greek: Πριγκίπισσα Ειρήνη της Ελλάδας και Δανίας; 13 February 1904 – 15 April 1974) was the fifth child and second daughter of King Constantine I of Greece and the former Princess Sophie of Prussia (sister of Kaiser Wilhelm II of Germany).
She was a member of the Royal Families of Greece and Italy.
Family and early life

Her Royal Highness Princess Irene of Greece and Denmark was born on 13 February 1904 in Athens.
She had three elder brothers, George (1890), Alexander (1893) and Paul (1901), and one elder sister, Helen (1896).
In 1927, her brother, George, announced her engagement to Prince Christian of Schaumburg-Lippe, a nephew of Christian X of Denmark, but no marriage occurred.
Princess Irene’s paternal grandparents were King George I of Greece and his Queen, Grand Duchess Olga Konstantinovna of Russia.
Her maternal grandparents were German Emperor Frederick III, and his Empress Consort, Victoria, Princess Royal.
Empress Victoria was a daughter of Prince Albert of Saxe-Coburg and Gotha and Queen Victoria of the United Kingdom.
Marriage

Shortly afterwards, the Greek princess had to officially renounce the Orthodox faith and convert to the Catholic religion, as required by the laws of the House of Savoy.
On 1 July 1939, Princess Irene married Prince Aimone, 4th Duke of Aosta (9 March 1900 – 29 January 1948).
She was also a bridesmaid at the wedding of her cousin, Princess Marina of Greece and Denmark
In March 1942, Irene, who was a trained nurse, headed a Red Cross hospital train going to Russia to repatriate wounded Italian soldiers.
Prince Aimone became the 4th Duke of Aosta on 3 March 1942, following the death of his elder brother, Amedeo.
After the Allied armistice with the Kingdom of Italy, Irene was interned by the Germans at the Hotel Ifen in Hirschegg, Austria, July 1944, along with her infant son, her sister-in-law and two nieces.
Prince Aimone died on 29 January 1948 in Buenos Aires.
Upon his death, his son Amedeo succeeded him as the 5th Duke of Aosta.
In June 1948, the family was allowed to return to Italy, and Irene spent the rest of her life living outside of Florence where she became a member of the Dominican Third Order and continued her social work.
Irene died on 15 April 1974 in Fiesole, Italy, after fighting a long illness.
Finally, in 1996, the ashes of the Duke and Duchess of Aosta were transferred to one of the necropolises of the House of Savoy, at the Basilica of Superga in Turin.
Ancestry

References

Edward Hanson, The Wandering Princess: Princess Helene of France, Duchess of Aosta (1871-1951) .



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
  AssignClass (000c8a11-f116-401f-9066-6d36bd93c4bb)
 Call ID: 000c8a11-f116-401f-9066-6d36bd93c4bb
  Args:
    type: :Woman
    source: :Princess_Irene_of_Greece_and_Denmark
  AssignClass (e1cf2656-c0bc-403c-9067-897731197731)
 Call ID: e1cf2656-c0bc-403c-9067-897731197731
  Args:
    type: :Person
    source: :Princess_Irene_of_Greece_and_Denmark
  AddLiteral (3e3d281e-450e-42cf-b099-2dfdbeeac4da)
 Call ID: 3e3d281e-450e-42cf-b099-2dfdbeeac4da
  Args:
    literal_value: 1904
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :Princess_Irene_of_Greece_and_Denmark
  AddLiteral (2c0e8d9f-8f9d-4740-9747-c6e6d1a4efa8)
 Call ID: 2c0e8d9f-8f9d-4740-9747-c6e6d1a4efa8
  Args:
    source: :Princess_Irene_of_Greece_and_Denmark
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1974
  AssignClass (7690d5e3-17bf-4421-b610-3f537caad377)
 Call ID: 7690d5e3-17bf-4421-b610-3f537caad377
  Args:
    type: :Man
    source: :King_Constantine_I_of_Greece
  AssignClass (f40eb4b0-3101-4487-8f41-4c4a09f579ac)
 Call ID: f40eb4b0-3101-4487-8f41-4c4a09f579ac
  Args:
    type: :Person
    source: :King_Constantine_I_of_Greece
  AssignClass (634823d8-f348-432f-8880-6c048cc028ce)
 Call ID: 634823d8-f348-432f-8880-6c048cc028ce
  Args:
    type: :Woman
    source: :Princess_Sophie_of_Prussia
  AssignClass (fe56e461-ad36-4934-8df0-5d4588437d95)
 Call ID: fe56e461-ad36-4934-8df0-5d4588437d95
  Args:
    type: :Person
    source: :Princess_Sophie_of_Prussia
  AddTriple (3a3a7ab3-86e4-4f5b-b429-2100bc2d61fa)
 Call ID: 3a3a7ab3-86e4-4f5b-b429-2100bc2d61fa
  Args:
    source: :Princess_Irene_of_Greece_and_Denmark
    target: :King_Constantine_I_of_Greece
    relation: :hasFather
  AddTriple (b9d786b2-35f9-4df1-9619-2c2e43575c75)
 Call ID: b9d786b2-35f9-4df1-9619-2c2e43575c75
  Args:
    source: :Princess_Irene_of_Greece_and_Denmark
    target: :Princess_Sophie_of_Prussia
    relation: :hasMother
  AssignClass (bb6f22da-3e77-4e6c-be38-68be5483fd5f)
 Call ID: bb6f22da-3e77-4e6c-be38-68be5483fd5f
  Args:
    type: :Man
    source: :George_of_Greece
  AssignClass (4afcfe9c-e03d-494b-94b2-fe56435fc7e9)
 Call ID: 4afcfe9c-e03d-494b-94b2-fe56435fc7e9
  Args:
    type: :Person
    source: :George_of_Greece
  AddTriple (3b6f0669-7f67-4571-9ab6-36121188bd33)
 Call ID: 3b6f0669-7f67-4571-9ab6-36121188bd33
  Args:
    source: :Princess_Irene_of_Greece_and_Denmark
    target: :George_of_Greece
    relation: :hasBrother
  AssignClass (1cac2ba2-f7a5-4b2a-8c17-d93167d46446)
 Call ID: 1cac2ba2-f7a5-4b2a-8c17-d93167d46446
  Args:
    type: :Man
    source: :Alexander_of_Greece
  AssignClass (7eac5d66-b0b2-4afa-bcdd-ffc46e6f2cd9)
 Call ID: 7eac5d66-b0b2-4afa-bcdd-ffc46e6f2cd9
  Args:
    type: :Person
    source: :Alexander_of_Greece
  AddTriple (d86d10e3-1443-42ac-821e-f64907913d00)
 Call ID: d86d10e3-1443-42ac-821e-f64907913d00
  Args:
    target: :Alexander_of_Greece
    relation: :hasBrother
    source: :Princess_Irene_of_Greece_and_Denmark
  AssignClass (d3de4d44-4e6d-464c-a027-04373961cf28)
 Call ID: d3de4d44-4e6d-464c-a027-04373961cf28
  Args:
    type: :Man
    source: :Paul_of_Greece
  AssignClass (d63d3dd4-9fde-44f4-a482-d96427146fb9)
 Call ID: d63d3dd4-9fde-44f4-a482-d96427146fb9
  Args:
    type: :Person
    source: :Paul_of_Greece
  AddTriple (812528f4-3f48-447d-a3b4-c90dfd9d9c1c)
 Call ID: 812528f4-3f48-447d-a3b4-c90dfd9d9c1c
  Args:
    source: :Princess_Irene_of_Greece_and_Denmark
    relation: :hasBrother
    target: :Paul_of_Greece
  AssignClass (f2ac2685-7fba-4bd9-b613-5c482a1ef744)
 Call ID: f2ac2685-7fba-4bd9-b613-5c482a1ef744
  Args:
    type: :Woman
    source: :Helen_of_Greece
  AssignClass (55252bf7-febe-41d4-a86a-edd03cdea369)
 Call ID: 55252bf7-febe-41d4-a86a-edd03cdea369
  Args:
    type: :Person
    source: :Helen_of_Greece
  AddTriple (81617d17-873f-4c54-b400-c8d9925af716)
 Call ID: 81617d17-873f-4c54-b400-c8d9925af716
  Args:
    relation: :hasSister
    target: :Helen_of_Greece
    source: :Princess_Irene_of_Greece_and_Denmark
  AssignClass (58206e29-a49b-446c-87b6-1b0eceb3cb48)
 Call ID: 58206e29-a49b-446c-87b6-1b0eceb3cb48
  Args:
    type: :Man
    source: :Prince_Aimone_4th_Duke_of_Aosta
  AssignClass (cd2ae7ea-37db-4d59-8d7e-bff8a132ec98)
 Call ID: cd2ae7ea-37db-4d59-8d7e-bff8a132ec98
  Args:
    type: :Person
    source: :Prince_Aimone_4th_Duke_of_Aosta
  AddLiteral (2c6f36a3-b423-4d32-b29a-440e8b09a9c2)
 Call ID: 2c6f36a3-b423-4d32-b29a-440e8b09a9c2
  Args:
    literal_value: 1939
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: :Princess_Irene_of_Greece_and_Denmark
  AddTriple (e081f8f1-82e0-4809-8564-0d23e8424fcf)
 Call ID: e081f8f1-82e0-4809-8564-0d23e8424fcf
  Args:
    source: :Princess_Irene_of_Greece_and_Denmark
    target: :Prince_Aimone_4th_Duke_of_Aosta
    relation: :hasRelation
  Finish (0de8adaa-918d-4ca0-83f7-2ff659ed5ca4)
 Call ID: 0de8adaa-918d-4ca0-83f7-2ff659ed5ca4
  Args: