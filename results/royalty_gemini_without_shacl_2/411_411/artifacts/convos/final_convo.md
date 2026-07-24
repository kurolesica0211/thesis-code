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
  AssignClass (258da9f3-6851-4d18-bfff-2c14478f1b31)
 Call ID: 258da9f3-6851-4d18-bfff-2c14478f1b31
  Args:
    type: :Man
    source: Christian_Louis_of_Mecklenburg
  AssignClass (43ceb405-b715-4e7e-a243-7009b204bc50)
 Call ID: 43ceb405-b715-4e7e-a243-7009b204bc50
  Args:
    type: :Person
    source: Christian_Louis_of_Mecklenburg
  AddLiteral (b178bc61-9ee5-4cbb-b0e2-2e98497bec2a)
 Call ID: b178bc61-9ee5-4cbb-b0e2-2e98497bec2a
  Args:
    literal_value: 1912
    relation: :hasBirthYear
    source: Christian_Louis_of_Mecklenburg
    literal_type: xsd:integer
  AddLiteral (9f223fa3-984d-4787-b784-ee350e312c7c)
 Call ID: 9f223fa3-984d-4787-b784-ee350e312c7c
  Args:
    relation: :hasDeathYear
    source: Christian_Louis_of_Mecklenburg
    literal_type: xsd:integer
    literal_value: 1996
  AssignClass (54bd2821-db9e-4a33-a5c6-5f2b99bacc51)
 Call ID: 54bd2821-db9e-4a33-a5c6-5f2b99bacc51
  Args:
    type: :Man
    source: Frederick_Francis_IV
  AssignClass (feebd32b-177f-4714-985b-c93baa88b158)
 Call ID: feebd32b-177f-4714-985b-c93baa88b158
  Args:
    source: Frederick_Francis_IV
    type: :Person
  AddTriple (2dd890c8-d069-49c4-8102-71dc318439c9)
 Call ID: 2dd890c8-d069-49c4-8102-71dc318439c9
  Args:
    relation: :isSonOf
    target: Frederick_Francis_IV
    source: Christian_Louis_of_Mecklenburg
  AssignClass (5287839f-d59d-4517-9a06-61671953d20e)
 Call ID: 5287839f-d59d-4517-9a06-61671953d20e
  Args:
    type: :Woman
    source: Alexandra_of_Hanover
  AssignClass (3a03de1c-ae10-4443-9c24-cf27e92d2277)
 Call ID: 3a03de1c-ae10-4443-9c24-cf27e92d2277
  Args:
    type: :Person
    source: Alexandra_of_Hanover
  AddTriple (55ee5fe6-28b1-41a1-accb-05859ed658e8)
 Call ID: 55ee5fe6-28b1-41a1-accb-05859ed658e8
  Args:
    relation: :isChildOf
    source: Christian_Louis_of_Mecklenburg
    target: Alexandra_of_Hanover
  AddTriple (7bbfc58c-39ba-4999-a357-b1320631748c)
 Call ID: 7bbfc58c-39ba-4999-a357-b1320631748c
  Args:
    relation: :isChildOf
    target: Frederick_Francis_IV
    source: Christian_Louis_of_Mecklenburg
  AddTriple (e70fa9b8-cbc6-46c2-806a-9188f43e58a4)
 Call ID: e70fa9b8-cbc6-46c2-806a-9188f43e58a4
  Args:
    relation: :isSonOf
    target: Alexandra_of_Hanover
    source: Christian_Louis_of_Mecklenburg
  AssignClass (6cc66dc5-b1cf-40b0-936e-20622899f04d)
 Call ID: 6cc66dc5-b1cf-40b0-936e-20622899f04d
  Args:
    source: Ernest_Augustus_of_Hanover
    type: :Man
  AssignClass (6bfacf11-ef32-4346-a589-6d660ad82470)
 Call ID: 6bfacf11-ef32-4346-a589-6d660ad82470
  Args:
    source: Ernest_Augustus_of_Hanover
    type: :Person
  AssignClass (3e7f9484-3deb-42f6-833a-50ace8a6bf70)
 Call ID: 3e7f9484-3deb-42f6-833a-50ace8a6bf70
  Args:
    type: :Woman
    source: Thyra_of_Denmark
  AssignClass (5e9fb1ef-2f6e-4feb-8619-20ed5818cfaf)
 Call ID: 5e9fb1ef-2f6e-4feb-8619-20ed5818cfaf
  Args:
    source: Thyra_of_Denmark
    type: :Person
  AddTriple (069c8290-a843-4123-8153-b8638a5ae39c)
 Call ID: 069c8290-a843-4123-8153-b8638a5ae39c
  Args:
    target: Ernest_Augustus_of_Hanover
    source: Alexandra_of_Hanover
    relation: :isDaughterOf
  AddTriple (24f58544-09f0-463f-8d03-5f849a58d7e6)
 Call ID: 24f58544-09f0-463f-8d03-5f849a58d7e6
  Args:
    target: Thyra_of_Denmark
    source: Alexandra_of_Hanover
    relation: :isDaughterOf
  AssignClass (805c7090-0a15-4af0-b70f-c7f5fb5d0171)
 Call ID: 805c7090-0a15-4af0-b70f-c7f5fb5d0171
  Args:
    type: :Woman
    source: Thyra_sister_of_Christian_Louis
  AssignClass (71e63724-88c5-444b-98d5-cede2ebb1cdb)
 Call ID: 71e63724-88c5-444b-98d5-cede2ebb1cdb
  Args:
    type: :Person
    source: Thyra_sister_of_Christian_Louis
  AddTriple (f278b3ba-4634-4a75-86ce-613bff5dc690)
 Call ID: f278b3ba-4634-4a75-86ce-613bff5dc690
  Args:
    target: Christian_Louis_of_Mecklenburg
    source: Thyra_sister_of_Christian_Louis
    relation: :isSisterOf
  AssignClass (0d3598eb-9c9b-4c84-95bf-3499d48a29bb)
 Call ID: 0d3598eb-9c9b-4c84-95bf-3499d48a29bb
  Args:
    type: :Woman
    source: Barbara_of_Prussia
  AssignClass (887e785d-a2cc-4f2d-8561-ed1e0a66cdfe)
 Call ID: 887e785d-a2cc-4f2d-8561-ed1e0a66cdfe
  Args:
    source: Barbara_of_Prussia
    type: :Person
  AddLiteral (fbd9ab36-b0bc-495c-944f-64ed9395fb77)
 Call ID: fbd9ab36-b0bc-495c-944f-64ed9395fb77
  Args:
    source: Barbara_of_Prussia
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1920
  AddLiteral (531fd1a3-bf36-4a1f-b982-06e0df7c38da)
 Call ID: 531fd1a3-bf36-4a1f-b982-06e0df7c38da
  Args:
    literal_value: 1994
    literal_type: xsd:integer
    source: Barbara_of_Prussia
    relation: :hasDeathYear
  AddLiteral (d74d1d13-63b7-4216-b6fa-ef1533823547)
 Call ID: d74d1d13-63b7-4216-b6fa-ef1533823547
  Args:
    source: Christian_Louis_of_Mecklenburg
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1954
  AddTriple (e1218376-fc88-41f5-b9a9-07848c53c6b7)
 Call ID: e1218376-fc88-41f5-b9a9-07848c53c6b7
  Args:
    relation: :hasRelation
    source: Christian_Louis_of_Mecklenburg
    target: Barbara_of_Prussia
  AssignClass (2321ee56-56d3-4fa0-96c1-45fd6e71d1f4)
 Call ID: 2321ee56-56d3-4fa0-96c1-45fd6e71d1f4
  Args:
    source: Sigismund_of_Prussia
    type: :Man
  AssignClass (66fffac9-9e63-4f42-9544-e159bc87248b)
 Call ID: 66fffac9-9e63-4f42-9544-e159bc87248b
  Args:
    type: :Person
    source: Sigismund_of_Prussia
  AssignClass (021b2699-84eb-42cc-8d44-41ec23dd4168)
 Call ID: 021b2699-84eb-42cc-8d44-41ec23dd4168
  Args:
    source: Charlotte_of_Saxe_Altenburg
    type: :Woman
  AssignClass (93e0999f-2906-4d75-8ca0-9221bda7283e)
 Call ID: 93e0999f-2906-4d75-8ca0-9221bda7283e
  Args:
    source: Charlotte_of_Saxe_Altenburg
    type: :Person
  AddTriple (b06e01c4-21da-4270-b8d4-e62f895ec3bc)
 Call ID: b06e01c4-21da-4270-b8d4-e62f895ec3bc
  Args:
    relation: :isDaughterOf
    source: Barbara_of_Prussia
    target: Sigismund_of_Prussia
  AddTriple (64510fa9-c9f7-4339-8e9e-27d1da669015)
 Call ID: 64510fa9-c9f7-4339-8e9e-27d1da669015
  Args:
    target: Charlotte_of_Saxe_Altenburg
    source: Barbara_of_Prussia
    relation: :isDaughterOf
  Finish (656fe671-75c0-4c59-97d2-3184744469f1)
 Call ID: 656fe671-75c0-4c59-97d2-3184744469f1
  Args: