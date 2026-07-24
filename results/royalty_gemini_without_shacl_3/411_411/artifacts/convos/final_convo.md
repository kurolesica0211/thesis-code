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
Duke Christian Louis of Mecklenburg (German: Christian-Ludwig Herzog zu Mecklenburg; 29 September 1912 – 18 July 1996) was the second son of the last reigning Grand Duke of Mecklenburg-Schwerin, Frederick Francis IV.
Early life

Born in Schloss Ludwigslust, as a member of an elder, Mecklenburg-Schwerin line of an ancient House of Mecklenburg, he was the second child of the reigning Grand Duke of Mecklenburg-Schwerin, Frederick Francis IV, and his wife, Princess Alexandra of Hanover, third child and second daughter of Ernest Augustus, Crown Prince of Hanover and Princess Thyra of Denmark.
After the abolition of the monarchy, in 1919 the family went at the invitation of Queen Alexandrine, consort of Christian X of Denmark and sister of the Grand Duke, into exile in Denmark, where they lived for a year in Sorgenfri Palace.
Later, the family returned to Mecklenburg and lived in Gelbensande, and from 1921 the family settled at Ludwigslust Castle.
After the war

When the war ended, Ludwigslust was first occupied by the British, but soon was transferred to the Soviet occupation, so that Christian Louis initially went with his family to Glücksburg Castle in Schleswig-Holstein.
Together with his sister Thyra, he took part in the ship tour organized by Queen Frederica and her husband King Paul of Greece in 1954, which became known as the “Cruise of the Kings” and was attended by over 100 royals from all over Europe.
Marriage and family

On 5 July 1954 in Glücksburg, Christian Louis married in a civil wedding Princess Barbara of Prussia (1920–1994), the daughter of Prince Sigismund of Prussia and his wife, Princess Charlotte of Saxe-Altenburg.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (b586b2c2-5311-47cf-93e2-08abfd2da6b3)
 Call ID: b586b2c2-5311-47cf-93e2-08abfd2da6b3
  Args:
    type: :Man
    source: :ChristianLouisOfMecklenburg
  AssignClass (a61de5fa-9fdf-4239-9889-02051b653c4d)
 Call ID: a61de5fa-9fdf-4239-9889-02051b653c4d
  Args:
    type: :Person
    source: :ChristianLouisOfMecklenburg
  AddLiteral (4452f045-a374-4f82-a982-bae8b195c66a)
 Call ID: 4452f045-a374-4f82-a982-bae8b195c66a
  Args:
    relation: :hasBirthYear
    literal_value: 1912
    literal_type: xsd:integer
    source: :ChristianLouisOfMecklenburg
  AddLiteral (bb4c7284-eaca-49ce-9634-51ea87252f60)
 Call ID: bb4c7284-eaca-49ce-9634-51ea87252f60
  Args:
    relation: :hasDeathYear
    literal_value: 1996
    literal_type: xsd:integer
    source: :ChristianLouisOfMecklenburg
  AssignClass (ccfb4afd-e115-4d81-80bf-1f15cec2ca8a)
 Call ID: ccfb4afd-e115-4d81-80bf-1f15cec2ca8a
  Args:
    type: :Man
    source: :FrederickFrancisIV
  AssignClass (71f7b6ab-07dc-49ab-90ba-c74d60c9aee8)
 Call ID: 71f7b6ab-07dc-49ab-90ba-c74d60c9aee8
  Args:
    type: :Person
    source: :FrederickFrancisIV
  AddTriple (263b954c-0df1-4737-b9c0-4260d85ae0cd)
 Call ID: 263b954c-0df1-4737-b9c0-4260d85ae0cd
  Args:
    source: :ChristianLouisOfMecklenburg
    target: :FrederickFrancisIV
    relation: :hasFather
  AssignClass (5f0495cf-a738-4fe4-be40-96a1ea7c7bc9)
 Call ID: 5f0495cf-a738-4fe4-be40-96a1ea7c7bc9
  Args:
    type: :Woman
    source: :AlexandraOfHanover
  AssignClass (481e34a2-e235-4050-95e8-1aa937a8f105)
 Call ID: 481e34a2-e235-4050-95e8-1aa937a8f105
  Args:
    type: :Person
    source: :AlexandraOfHanover
  AddTriple (93807909-c86d-4dd7-8e94-f8ffd00d4daf)
 Call ID: 93807909-c86d-4dd7-8e94-f8ffd00d4daf
  Args:
    relation: :hasMother
    source: :ChristianLouisOfMecklenburg
    target: :AlexandraOfHanover
  AssignClass (548d5d5e-93c2-424d-80e0-a88ddf650b3f)
 Call ID: 548d5d5e-93c2-424d-80e0-a88ddf650b3f
  Args:
    type: :Man
    source: :ErnestAugustusCrownPrinceOfHanover
  AssignClass (39749fa5-3bb9-44c9-b612-f3f225491df7)
 Call ID: 39749fa5-3bb9-44c9-b612-f3f225491df7
  Args:
    type: :Person
    source: :ErnestAugustusCrownPrinceOfHanover
  AddTriple (b7cdba6b-f7b7-4b0c-ae63-67b797f29366)
 Call ID: b7cdba6b-f7b7-4b0c-ae63-67b797f29366
  Args:
    target: :ErnestAugustusCrownPrinceOfHanover
    source: :AlexandraOfHanover
    relation: :hasFather
  AssignClass (369a2916-eb83-4e06-a2df-369f6d968f93)
 Call ID: 369a2916-eb83-4e06-a2df-369f6d968f93
  Args:
    type: :Woman
    source: :ThyraOfDenmark
  AssignClass (9bab32ac-5d24-4bba-960f-2b9fe59f462b)
 Call ID: 9bab32ac-5d24-4bba-960f-2b9fe59f462b
  Args:
    type: :Person
    source: :ThyraOfDenmark
  AddTriple (f8fe7022-e88b-4892-8563-f3c6e73de2c6)
 Call ID: f8fe7022-e88b-4892-8563-f3c6e73de2c6
  Args:
    relation: :hasMother
    source: :AlexandraOfHanover
    target: :ThyraOfDenmark
  AssignClass (cd0d5dca-92b0-4407-a0be-325e2593a275)
 Call ID: cd0d5dca-92b0-4407-a0be-325e2593a275
  Args:
    type: :Woman
    source: :ThyraOfMecklenburg
  AssignClass (62d6a6f3-6800-4388-b187-7393bd13ab5d)
 Call ID: 62d6a6f3-6800-4388-b187-7393bd13ab5d
  Args:
    type: :Person
    source: :ThyraOfMecklenburg
  AddTriple (49074f51-4d46-4c79-904a-0315c1e324af)
 Call ID: 49074f51-4d46-4c79-904a-0315c1e324af
  Args:
    target: :ThyraOfMecklenburg
    source: :ChristianLouisOfMecklenburg
    relation: :hasSister
  AddTriple (368cf7c9-094a-4523-91e2-746712122d09)
 Call ID: 368cf7c9-094a-4523-91e2-746712122d09
  Args:
    target: :FrederickFrancisIV
    source: :ThyraOfMecklenburg
    relation: :hasFather
  AddTriple (9c081834-aff3-4ce6-bcd3-d82a70ededb9)
 Call ID: 9c081834-aff3-4ce6-bcd3-d82a70ededb9
  Args:
    target: :AlexandraOfHanover
    source: :ThyraOfMecklenburg
    relation: :hasMother
  AssignClass (7190b633-1431-43e6-b03e-a28d83e859c8)
 Call ID: 7190b633-1431-43e6-b03e-a28d83e859c8
  Args:
    type: :Woman
    source: :BarbaraOfPrussia
  AssignClass (83a0ff0f-f5a8-4a08-b369-28b131f3bc81)
 Call ID: 83a0ff0f-f5a8-4a08-b369-28b131f3bc81
  Args:
    type: :Person
    source: :BarbaraOfPrussia
  AddLiteral (63164659-090c-41c0-80a9-892fbd2c7ec1)
 Call ID: 63164659-090c-41c0-80a9-892fbd2c7ec1
  Args:
    literal_value: 1954
    relation: :hasMarriageYear
    source: :ChristianLouisOfMecklenburg
    literal_type: xsd:integer
  AddTriple (8d99aae9-eb66-4de3-a902-5f2b74794e1b)
 Call ID: 8d99aae9-eb66-4de3-a902-5f2b74794e1b
  Args:
    relation: :hasRelation
    source: :ChristianLouisOfMecklenburg
    target: :BarbaraOfPrussia
  AddLiteral (e2bf7423-a951-47a2-b6f9-7c25dc76f6a3)
 Call ID: e2bf7423-a951-47a2-b6f9-7c25dc76f6a3
  Args:
    literal_value: 1920
    relation: :hasBirthYear
    source: :BarbaraOfPrussia
    literal_type: xsd:integer
  AddLiteral (1ccbc4ed-f8d2-417b-9932-fb074e196f0b)
 Call ID: 1ccbc4ed-f8d2-417b-9932-fb074e196f0b
  Args:
    literal_value: 1994
    relation: :hasDeathYear
    source: :BarbaraOfPrussia
    literal_type: xsd:integer
  AssignClass (62862f98-df3d-4c2b-9c4d-5fcf19b91ece)
 Call ID: 62862f98-df3d-4c2b-9c4d-5fcf19b91ece
  Args:
    type: :Man
    source: :SigismundOfPrussia
  AssignClass (aacdec71-9c12-4e74-8221-38fa807cb02f)
 Call ID: aacdec71-9c12-4e74-8221-38fa807cb02f
  Args:
    type: :Person
    source: :SigismundOfPrussia
  AddTriple (6849c9e8-f53c-4c91-bfe5-39ea35780dde)
 Call ID: 6849c9e8-f53c-4c91-bfe5-39ea35780dde
  Args:
    target: :SigismundOfPrussia
    source: :BarbaraOfPrussia
    relation: :hasFather
  AssignClass (aa9bfcd4-41de-4111-b348-a30717fed9f9)
 Call ID: aa9bfcd4-41de-4111-b348-a30717fed9f9
  Args:
    type: :Woman
    source: :CharlotteOfSaxeAltenburg
  AssignClass (09eb6f9e-d0e1-4e66-b3cd-9f49015f7f8a)
 Call ID: 09eb6f9e-d0e1-4e66-b3cd-9f49015f7f8a
  Args:
    type: :Person
    source: :CharlotteOfSaxeAltenburg
  AddTriple (700a9908-8ee6-4b35-aba2-4b4f65ae6a89)
 Call ID: 700a9908-8ee6-4b35-aba2-4b4f65ae6a89
  Args:
    target: :CharlotteOfSaxeAltenburg
    source: :BarbaraOfPrussia
    relation: :hasMother
  Finish (794a32d0-83cc-4a3b-9464-a944944aa09a)
 Call ID: 794a32d0-83cc-4a3b-9464-a944944aa09a
  Args: