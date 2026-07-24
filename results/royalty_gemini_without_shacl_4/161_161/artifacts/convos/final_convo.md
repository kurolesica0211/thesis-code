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
  AssignClass (afe68690-2b29-43e7-a3e1-38bcf21fced6)
 Call ID: afe68690-2b29-43e7-a3e1-38bcf21fced6
  Args:
    source: :Princess_Irene_of_Greece_and_Denmark
    type: :Woman
  AssignClass (8fe67766-0559-4add-8c14-d101a292b0ff)
 Call ID: 8fe67766-0559-4add-8c14-d101a292b0ff
  Args:
    type: :Person
    source: :Princess_Irene_of_Greece_and_Denmark
  AddLiteral (9887eccd-93b8-4b3e-a286-93c1396aa0cc)
 Call ID: 9887eccd-93b8-4b3e-a286-93c1396aa0cc
  Args:
    source: :Princess_Irene_of_Greece_and_Denmark
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1904
  AddLiteral (4a97b55e-ad7e-4173-8eae-f637db253c2d)
 Call ID: 4a97b55e-ad7e-4173-8eae-f637db253c2d
  Args:
    source: :Princess_Irene_of_Greece_and_Denmark
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1974
  AssignClass (6f116e76-dd31-41f6-9a1f-1d6b46150631)
 Call ID: 6f116e76-dd31-41f6-9a1f-1d6b46150631
  Args:
    type: :Man
    source: :King_Constantine_I_of_Greece
  AssignClass (0d6312f5-e33e-43c1-bf05-1989e6a3389a)
 Call ID: 0d6312f5-e33e-43c1-bf05-1989e6a3389a
  Args:
    type: :Person
    source: :King_Constantine_I_of_Greece
  AssignClass (8e46f1b8-fba1-4141-859b-856773454dc7)
 Call ID: 8e46f1b8-fba1-4141-859b-856773454dc7
  Args:
    source: :Princess_Sophie_of_Prussia
    type: :Woman
  AssignClass (8e5a794b-7397-43fd-afd1-b09953b735e5)
 Call ID: 8e5a794b-7397-43fd-afd1-b09953b735e5
  Args:
    type: :Person
    source: :Princess_Sophie_of_Prussia
  AddTriple (a71d7fa7-747f-4278-9531-b33a283b5541)
 Call ID: a71d7fa7-747f-4278-9531-b33a283b5541
  Args:
    relation: :hasFather
    source: :Princess_Irene_of_Greece_and_Denmark
    target: :King_Constantine_I_of_Greece
  AddTriple (cd2c3953-0c3d-4de6-9518-421e87bcfa7d)
 Call ID: cd2c3953-0c3d-4de6-9518-421e87bcfa7d
  Args:
    relation: :hasMother
    source: :Princess_Irene_of_Greece_and_Denmark
    target: :Princess_Sophie_of_Prussia
  AssignClass (8c8350ff-ae43-4a25-abe5-7671ee088e63)
 Call ID: 8c8350ff-ae43-4a25-abe5-7671ee088e63
  Args:
    type: :Man
    source: :Prince_George_of_Greece
  AssignClass (16b5f27b-1e1a-4205-8942-eeda71b8ab78)
 Call ID: 16b5f27b-1e1a-4205-8942-eeda71b8ab78
  Args:
    source: :Prince_George_of_Greece
    type: :Person
  AddTriple (13b267ee-440d-4519-9768-8b29e29e4ad5)
 Call ID: 13b267ee-440d-4519-9768-8b29e29e4ad5
  Args:
    relation: :hasBrother
    source: :Princess_Irene_of_Greece_and_Denmark
    target: :Prince_George_of_Greece
  AssignClass (e1ee1058-a2e1-4d40-8928-3c1b6fec6775)
 Call ID: e1ee1058-a2e1-4d40-8928-3c1b6fec6775
  Args:
    type: :Man
    source: :Prince_Alexander_of_Greece
  AssignClass (bace89a6-10aa-4aba-af08-85e83e609980)
 Call ID: bace89a6-10aa-4aba-af08-85e83e609980
  Args:
    type: :Person
    source: :Prince_Alexander_of_Greece
  AddTriple (56bdb4a9-1714-4444-b027-d31fee06f786)
 Call ID: 56bdb4a9-1714-4444-b027-d31fee06f786
  Args:
    relation: :hasBrother
    source: :Princess_Irene_of_Greece_and_Denmark
    target: :Prince_Alexander_of_Greece
  AssignClass (87f780b1-22c8-4c34-bf20-bfb947422ccc)
 Call ID: 87f780b1-22c8-4c34-bf20-bfb947422ccc
  Args:
    source: :Prince_Paul_of_Greece
    type: :Man
  AssignClass (83b2da82-3964-4c13-81f6-33061606e291)
 Call ID: 83b2da82-3964-4c13-81f6-33061606e291
  Args:
    source: :Prince_Paul_of_Greece
    type: :Person
  AddTriple (77bd0e6a-9b71-4360-be5e-9c9f2bc640f0)
 Call ID: 77bd0e6a-9b71-4360-be5e-9c9f2bc640f0
  Args:
    source: :Princess_Irene_of_Greece_and_Denmark
    relation: :hasBrother
    target: :Prince_Paul_of_Greece
  AssignClass (187681f2-9570-42d9-9cf0-2abffe1f0209)
 Call ID: 187681f2-9570-42d9-9cf0-2abffe1f0209
  Args:
    source: :Princess_Helen_of_Greece
    type: :Woman
  AssignClass (38cf6e3c-8179-4060-944d-f8489b493b48)
 Call ID: 38cf6e3c-8179-4060-944d-f8489b493b48
  Args:
    type: :Person
    source: :Princess_Helen_of_Greece
  AddTriple (235a3a37-c7a7-443b-ad7b-5714252cb302)
 Call ID: 235a3a37-c7a7-443b-ad7b-5714252cb302
  Args:
    target: :Princess_Helen_of_Greece
    relation: :hasSister
    source: :Princess_Irene_of_Greece_and_Denmark
  AssignClass (8de50f31-9041-4389-bf04-f93f372e03ec)
 Call ID: 8de50f31-9041-4389-bf04-f93f372e03ec
  Args:
    type: :Man
    source: :Prince_Aimone_4th_Duke_of_Aosta
  AssignClass (a2eb182c-1126-4621-bb04-db392eac1be1)
 Call ID: a2eb182c-1126-4621-bb04-db392eac1be1
  Args:
    source: :Prince_Aimone_4th_Duke_of_Aosta
    type: :Person
  AddLiteral (23a26995-836d-4cae-abb5-8ddd989d4a2f)
 Call ID: 23a26995-836d-4cae-abb5-8ddd989d4a2f
  Args:
    relation: :hasMarriageYear
    source: :Princess_Irene_of_Greece_and_Denmark
    literal_value: 1939
    literal_type: xsd:integer
  AddTriple (725293e2-4f9d-4171-8f25-985ba5f3534f)
 Call ID: 725293e2-4f9d-4171-8f25-985ba5f3534f
  Args:
    relation: :hasRelation
    source: :Princess_Irene_of_Greece_and_Denmark
    target: :Prince_Aimone_4th_Duke_of_Aosta
  AddLiteral (608c6fc7-4358-4d50-b5b4-288806ab9899)
 Call ID: 608c6fc7-4358-4d50-b5b4-288806ab9899
  Args:
    source: :Prince_Aimone_4th_Duke_of_Aosta
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1900
  AddLiteral (8bc024d6-5e0c-4a11-9a37-b411280a0062)
 Call ID: 8bc024d6-5e0c-4a11-9a37-b411280a0062
  Args:
    literal_type: xsd:integer
    literal_value: 1948
    relation: :hasDeathYear
    source: :Prince_Aimone_4th_Duke_of_Aosta
  AssignClass (8e5b8fed-4533-4c76-9f68-f09e81a5e185)
 Call ID: 8e5b8fed-4533-4c76-9f68-f09e81a5e185
  Args:
    type: :Man
    source: :Amedeo_5th_Duke_of_Aosta
  AssignClass (c38262c4-a29d-4331-af60-0c5e416f4d19)
 Call ID: c38262c4-a29d-4331-af60-0c5e416f4d19
  Args:
    type: :Person
    source: :Amedeo_5th_Duke_of_Aosta
  AddTriple (fa61379f-9b89-4600-9239-cfa6e77ca817)
 Call ID: fa61379f-9b89-4600-9239-cfa6e77ca817
  Args:
    target: :Amedeo_5th_Duke_of_Aosta
    source: :Princess_Irene_of_Greece_and_Denmark
    relation: :hasSon
  AddTriple (c6cac590-f0d5-4cd8-8357-5e6a5704af70)
 Call ID: c6cac590-f0d5-4cd8-8357-5e6a5704af70
  Args:
    target: :Prince_Aimone_4th_Duke_of_Aosta
    source: :Amedeo_5th_Duke_of_Aosta
    relation: :hasFather
  Finish (a2362a42-fec3-44dc-8f28-13fe4f8c34c3)
 Call ID: a2362a42-fec3-44dc-8f28-13fe4f8c34c3
  Args: