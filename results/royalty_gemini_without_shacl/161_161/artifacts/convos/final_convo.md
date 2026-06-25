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
  AssignClass (eafaa95a-050b-43bc-9931-e6aec9125346)
 Call ID: eafaa95a-050b-43bc-9931-e6aec9125346
  Args:
    source: :Irene_of_Greece_and_Denmark
    type: :Woman
  AssignClass (b6984f0e-042e-4071-bcc0-2c37490387ec)
 Call ID: b6984f0e-042e-4071-bcc0-2c37490387ec
  Args:
    source: :Irene_of_Greece_and_Denmark
    type: :Person
  AddLiteral (47b7e77f-e5c5-4f0b-8862-445ffdcc2092)
 Call ID: 47b7e77f-e5c5-4f0b-8862-445ffdcc2092
  Args:
    literal_value: 1904
    source: :Irene_of_Greece_and_Denmark
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (3973d27c-288e-423d-8440-f33e1dfd4668)
 Call ID: 3973d27c-288e-423d-8440-f33e1dfd4668
  Args:
    source: :Irene_of_Greece_and_Denmark
    literal_value: 1974
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (dff7a796-5a56-4e86-bb74-a45e1f0b91e0)
 Call ID: dff7a796-5a56-4e86-bb74-a45e1f0b91e0
  Args:
    type: :Man
    source: :Constantine_I_of_Greece
  AssignClass (a1760cea-f3d8-44ae-9409-8382cb607ba9)
 Call ID: a1760cea-f3d8-44ae-9409-8382cb607ba9
  Args:
    type: :Person
    source: :Constantine_I_of_Greece
  AssignClass (bb737e7c-cb42-45ec-bfaf-3292b1c2874c)
 Call ID: bb737e7c-cb42-45ec-bfaf-3292b1c2874c
  Args:
    source: :Sophie_of_Prussia
    type: :Woman
  AssignClass (29e62a0e-a853-4734-8782-4650ea56a5dd)
 Call ID: 29e62a0e-a853-4734-8782-4650ea56a5dd
  Args:
    type: :Person
    source: :Sophie_of_Prussia
  AddTriple (43886223-1211-45f0-a215-97f3f7cbb3f1)
 Call ID: 43886223-1211-45f0-a215-97f3f7cbb3f1
  Args:
    source: :Irene_of_Greece_and_Denmark
    target: :Constantine_I_of_Greece
    relation: :hasFather
  AddTriple (5986fd4a-d310-41b6-98f7-d04a40449e6e)
 Call ID: 5986fd4a-d310-41b6-98f7-d04a40449e6e
  Args:
    relation: :hasMother
    source: :Irene_of_Greece_and_Denmark
    target: :Sophie_of_Prussia
  AssignClass (b26b61d4-5a07-4486-9072-6af5fb515f98)
 Call ID: b26b61d4-5a07-4486-9072-6af5fb515f98
  Args:
    source: :George_of_Greece
    type: :Man
  AssignClass (e783a982-1713-4992-9364-5e547d533cc6)
 Call ID: e783a982-1713-4992-9364-5e547d533cc6
  Args:
    source: :George_of_Greece
    type: :Person
  AssignClass (019ac098-b77b-447b-bf24-99734cd1101b)
 Call ID: 019ac098-b77b-447b-bf24-99734cd1101b
  Args:
    type: :Man
    source: :Alexander_of_Greece
  AssignClass (a6c0e2a5-2476-4a63-901d-58aed8b3355e)
 Call ID: a6c0e2a5-2476-4a63-901d-58aed8b3355e
  Args:
    type: :Person
    source: :Alexander_of_Greece
  AssignClass (7de34042-13c7-44d6-b4bb-1e0bd00ad17d)
 Call ID: 7de34042-13c7-44d6-b4bb-1e0bd00ad17d
  Args:
    source: :Paul_of_Greece
    type: :Man
  AssignClass (b3d5875a-ffe6-49b6-8d6a-5ed3ea2da08c)
 Call ID: b3d5875a-ffe6-49b6-8d6a-5ed3ea2da08c
  Args:
    type: :Person
    source: :Paul_of_Greece
  AssignClass (32678c70-257c-4476-b204-d7fd7dc98c28)
 Call ID: 32678c70-257c-4476-b204-d7fd7dc98c28
  Args:
    type: :Woman
    source: :Helen_of_Greece
  AssignClass (727b14b1-2dd8-44ad-aab3-4d7513ede054)
 Call ID: 727b14b1-2dd8-44ad-aab3-4d7513ede054
  Args:
    source: :Helen_of_Greece
    type: :Person
  AddTriple (66f88799-a371-4a52-9e67-cf92d4f3bd4d)
 Call ID: 66f88799-a371-4a52-9e67-cf92d4f3bd4d
  Args:
    relation: :isSiblingOf
    target: :George_of_Greece
    source: :Irene_of_Greece_and_Denmark
  AddTriple (552b46a1-1e34-4d7a-a241-bdf97c8556b1)
 Call ID: 552b46a1-1e34-4d7a-a241-bdf97c8556b1
  Args:
    relation: :isSiblingOf
    source: :Irene_of_Greece_and_Denmark
    target: :Alexander_of_Greece
  AddTriple (16749926-86e0-4d49-8bed-8750e6194c50)
 Call ID: 16749926-86e0-4d49-8bed-8750e6194c50
  Args:
    target: :Paul_of_Greece
    source: :Irene_of_Greece_and_Denmark
    relation: :isSiblingOf
  AddTriple (3030b17b-3a55-4dd6-84ac-0aee184a5a08)
 Call ID: 3030b17b-3a55-4dd6-84ac-0aee184a5a08
  Args:
    source: :Irene_of_Greece_and_Denmark
    target: :Helen_of_Greece
    relation: :isSiblingOf
  AssignClass (e9c40577-f8e5-40d0-8b94-5303ccd2c101)
 Call ID: e9c40577-f8e5-40d0-8b94-5303ccd2c101
  Args:
    type: :Man
    source: :Aimone_4th_Duke_of_Aosta
  AssignClass (6064ac6e-c54e-4dad-bade-97c119931071)
 Call ID: 6064ac6e-c54e-4dad-bade-97c119931071
  Args:
    source: :Aimone_4th_Duke_of_Aosta
    type: :Person
  AddLiteral (9f08cf10-3337-437f-b6c2-06c9e8a3693e)
 Call ID: 9f08cf10-3337-437f-b6c2-06c9e8a3693e
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: :Irene_of_Greece_and_Denmark
    literal_value: 1939
  AddTriple (cd037044-5377-4622-8ba1-596eab803d97)
 Call ID: cd037044-5377-4622-8ba1-596eab803d97
  Args:
    relation: :hasRelation
    source: :Irene_of_Greece_and_Denmark
    target: :Aimone_4th_Duke_of_Aosta
  AssignClass (2936c518-dba3-41aa-9622-26e220206e98)
 Call ID: 2936c518-dba3-41aa-9622-26e220206e98
  Args:
    source: :Amedeo_5th_Duke_of_Aosta
    type: :Man
  AssignClass (052dbca5-a3b8-4c5e-94d6-1843279d74f9)
 Call ID: 052dbca5-a3b8-4c5e-94d6-1843279d74f9
  Args:
    source: :Amedeo_5th_Duke_of_Aosta
    type: :Person
  AddTriple (b7806470-0037-4c2c-857a-f6bd41a87b7a)
 Call ID: b7806470-0037-4c2c-857a-f6bd41a87b7a
  Args:
    target: :Irene_of_Greece_and_Denmark
    source: :Amedeo_5th_Duke_of_Aosta
    relation: :hasMother
  AddTriple (9fda83ba-a1ee-4173-b2c8-3c8bccf0819b)
 Call ID: 9fda83ba-a1ee-4173-b2c8-3c8bccf0819b
  Args:
    relation: :hasFather
    target: :Aimone_4th_Duke_of_Aosta
    source: :Amedeo_5th_Duke_of_Aosta
  Finish (0ebe4e3c-a663-4775-8c69-79a3dbf441f2)
 Call ID: 0ebe4e3c-a663-4775-8c69-79a3dbf441f2
  Args: