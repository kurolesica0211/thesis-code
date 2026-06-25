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
Princess Marie Alexandra of Baden (Marie Alexandra Thyra Victoria Louise Carola Hilda; 1 August 1902 – 29 January 1944) was a Hessian princess by marriage.
Family

She was the only daughter and elder child of Prince Maximilian of Baden (1867–1929) and Princess Marie Louise of Hanover and Cumberland.
Her paternal grandparents were Prince Wilhelm of Baden (1829–97) and Princess Maria Maximilianovna of Leuchtenberg (1841–1914), a daughter of Maximilian, Duke of Leuchtenberg (1817–52) and Grand Duchess Maria Nikolaevna (1819–1876).
Princess Marie-Louise of Hanover (1879–1948) was a daughter of Ernest Augustus, Crown Prince of Hanover, claimant of the annexed Kingdom of Hanover.
Marriage

On 17 September 1924, she married her fourth cousin Prince Wolfgang of Hesse (1896–1989).
Death

Princess Marie Alexandra was killed in an attack by the U.S. Army Air Forces during an air-raid on Frankfurt am Main on 29–30 January 1944 during World War II.
She and seven other women, who were aid workers, were killed when the cellar, in which they had taken refuge, collapsed under the weight of the building, rendering Marie Alexandra's body barely recognisable.



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
  AssignClass (194c514e-be8f-4b88-b2a1-2ce584123e98)
 Call ID: 194c514e-be8f-4b88-b2a1-2ce584123e98
  Args:
    source: Princess_Marie_Alexandra_of_Baden
    type: :Woman
  AssignClass (14b28081-d15b-4ec7-8158-41b8d55fb4f8)
 Call ID: 14b28081-d15b-4ec7-8158-41b8d55fb4f8
  Args:
    type: :Man
    source: Prince_Maximilian_of_Baden
  AssignClass (adfe43b3-f163-4977-a3e7-d344d49931dd)
 Call ID: adfe43b3-f163-4977-a3e7-d344d49931dd
  Args:
    type: :Woman
    source: Princess_Marie_Louise_of_Hanover_and_Cumberland
  AssignClass (439787c3-e2ec-476e-a5fc-231e966b4e93)
 Call ID: 439787c3-e2ec-476e-a5fc-231e966b4e93
  Args:
    source: Prince_Wilhelm_of_Baden
    type: :Man
  AssignClass (274d4068-a530-4e7a-a9e8-ab1db2a0a115)
 Call ID: 274d4068-a530-4e7a-a9e8-ab1db2a0a115
  Args:
    source: Princess_Maria_Maximilianovna_of_Leuchtenberg
    type: :Woman
  AssignClass (20908605-fe0a-451c-a1a8-13265b8c7df5)
 Call ID: 20908605-fe0a-451c-a1a8-13265b8c7df5
  Args:
    source: Maximilian_Duke_of_Leuchtenberg
    type: :Man
  AssignClass (050bc219-56de-496a-a421-282def3357c1)
 Call ID: 050bc219-56de-496a-a421-282def3357c1
  Args:
    type: :Woman
    source: Grand_Duchess_Maria_Nikolaevna
  AssignClass (225f596e-c21a-463f-b12e-3a8d4408105b)
 Call ID: 225f596e-c21a-463f-b12e-3a8d4408105b
  Args:
    source: Ernest_Augustus_Crown_Prince_of_Hanover
    type: :Man
  AssignClass (4cc7641c-6ece-4473-b768-124c69b3252c)
 Call ID: 4cc7641c-6ece-4473-b768-124c69b3252c
  Args:
    type: :Man
    source: Prince_Wolfgang_of_Hesse
  AddLiteral (129628ca-5085-463a-9a6d-6bca6fde1cb4)
 Call ID: 129628ca-5085-463a-9a6d-6bca6fde1cb4
  Args:
    source: Princess_Marie_Alexandra_of_Baden
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1902
  AddLiteral (1db62370-123d-4cbb-8095-a2ae60afb7f8)
 Call ID: 1db62370-123d-4cbb-8095-a2ae60afb7f8
  Args:
    source: Princess_Marie_Alexandra_of_Baden
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1944
  AddLiteral (4483cdb1-ccaa-40e6-a746-c64704cb4f71)
 Call ID: 4483cdb1-ccaa-40e6-a746-c64704cb4f71
  Args:
    literal_value: 1867
    relation: :hasBirthYear
    source: Prince_Maximilian_of_Baden
    literal_type: xsd:integer
  AddLiteral (51a5eb02-8c13-4ae5-b32f-674d5fafe676)
 Call ID: 51a5eb02-8c13-4ae5-b32f-674d5fafe676
  Args:
    source: Prince_Maximilian_of_Baden
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1929
  AddLiteral (1928c715-95e4-4d1a-a3d8-d02eabcea57f)
 Call ID: 1928c715-95e4-4d1a-a3d8-d02eabcea57f
  Args:
    literal_value: 1879
    relation: :hasBirthYear
    source: Princess_Marie_Louise_of_Hanover_and_Cumberland
    literal_type: xsd:integer
  AddLiteral (b4f8a50e-3160-43c4-af27-3ab28afb15f4)
 Call ID: b4f8a50e-3160-43c4-af27-3ab28afb15f4
  Args:
    relation: :hasDeathYear
    source: Princess_Marie_Louise_of_Hanover_and_Cumberland
    literal_type: xsd:integer
    literal_value: 1948
  AddLiteral (92a5389d-b93d-4f2a-a5d2-d36bdbec5a0d)
 Call ID: 92a5389d-b93d-4f2a-a5d2-d36bdbec5a0d
  Args:
    relation: :hasBirthYear
    source: Prince_Wilhelm_of_Baden
    literal_type: xsd:integer
    literal_value: 1829
  AddLiteral (5d79a137-8dc5-4da6-9354-85aec910d094)
 Call ID: 5d79a137-8dc5-4da6-9354-85aec910d094
  Args:
    literal_value: 1897
    literal_type: xsd:integer
    source: Prince_Wilhelm_of_Baden
    relation: :hasDeathYear
  AddLiteral (6770b2b8-8404-4fdb-894b-31f2848ddcf3)
 Call ID: 6770b2b8-8404-4fdb-894b-31f2848ddcf3
  Args:
    literal_value: 1841
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Princess_Maria_Maximilianovna_of_Leuchtenberg
  AddLiteral (2f17d641-fe0b-420a-bc1d-94f6ca129a5f)
 Call ID: 2f17d641-fe0b-420a-bc1d-94f6ca129a5f
  Args:
    literal_value: 1914
    relation: :hasDeathYear
    source: Princess_Maria_Maximilianovna_of_Leuchtenberg
    literal_type: xsd:integer
  AddLiteral (3ca69b82-bf90-478b-aadd-273474d503ed)
 Call ID: 3ca69b82-bf90-478b-aadd-273474d503ed
  Args:
    literal_value: 1817
    relation: :hasBirthYear
    source: Maximilian_Duke_of_Leuchtenberg
    literal_type: xsd:integer
  AddLiteral (65375dc6-28b3-403f-ba47-cd30c1da82a8)
 Call ID: 65375dc6-28b3-403f-ba47-cd30c1da82a8
  Args:
    literal_value: 1852
    source: Maximilian_Duke_of_Leuchtenberg
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddLiteral (6d2407f7-be0b-4e9a-baf0-b337dca9c231)
 Call ID: 6d2407f7-be0b-4e9a-baf0-b337dca9c231
  Args:
    relation: :hasBirthYear
    source: Grand_Duchess_Maria_Nikolaevna
    literal_type: xsd:integer
    literal_value: 1819
  AddLiteral (aa337dd7-9694-4131-bbc6-bebe6b111e41)
 Call ID: aa337dd7-9694-4131-bbc6-bebe6b111e41
  Args:
    literal_value: 1876
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Grand_Duchess_Maria_Nikolaevna
  AddLiteral (c8840e94-5d5d-4947-85e1-c5b1ab62d3ee)
 Call ID: c8840e94-5d5d-4947-85e1-c5b1ab62d3ee
  Args:
    literal_value: 1896
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Prince_Wolfgang_of_Hesse
  AddLiteral (1e94b14a-0ae7-4531-8232-d51dd53642f1)
 Call ID: 1e94b14a-0ae7-4531-8232-d51dd53642f1
  Args:
    literal_value: 1989
    relation: :hasDeathYear
    source: Prince_Wolfgang_of_Hesse
    literal_type: xsd:integer
  AddLiteral (ffc431d8-df07-4ab7-ad1d-df3435f1847f)
 Call ID: ffc431d8-df07-4ab7-ad1d-df3435f1847f
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Princess_Marie_Alexandra_of_Baden
    literal_value: 1924
  AddTriple (d04783d0-8576-46b8-9c51-014c3ce57745)
 Call ID: d04783d0-8576-46b8-9c51-014c3ce57745
  Args:
    target: Prince_Maximilian_of_Baden
    source: Princess_Marie_Alexandra_of_Baden
    relation: :hasFather
  AddTriple (df5c43e4-13f4-43d2-89c1-c6aa2132eaad)
 Call ID: df5c43e4-13f4-43d2-89c1-c6aa2132eaad
  Args:
    target: Princess_Marie_Louise_of_Hanover_and_Cumberland
    source: Princess_Marie_Alexandra_of_Baden
    relation: :hasMother
  AddTriple (b1a44268-4e6d-4f49-ab21-136b02cd6f4f)
 Call ID: b1a44268-4e6d-4f49-ab21-136b02cd6f4f
  Args:
    target: Prince_Wilhelm_of_Baden
    relation: :hasFather
    source: Princess_Marie_Alexandra_of_Baden
  AddTriple (8032044f-3b89-42c0-a309-b64ed74eddb7)
 Call ID: 8032044f-3b89-42c0-a309-b64ed74eddb7
  Args:
    target: Princess_Maria_Maximilianovna_of_Leuchtenberg
    source: Princess_Marie_Alexandra_of_Baden
    relation: :hasMother
  AddTriple (bfb3282b-a3bc-4f6e-9d17-936b0f486910)
 Call ID: bfb3282b-a3bc-4f6e-9d17-936b0f486910
  Args:
    source: Princess_Maria_Maximilianovna_of_Leuchtenberg
    relation: :hasFather
    target: Maximilian_Duke_of_Leuchtenberg
  AddTriple (a3f846b6-4430-4b9d-8256-488e0fca329c)
 Call ID: a3f846b6-4430-4b9d-8256-488e0fca329c
  Args:
    target: Grand_Duchess_Maria_Nikolaevna
    relation: :hasMother
    source: Princess_Maria_Maximilianovna_of_Leuchtenberg
  AddTriple (2d68688f-168f-4d9f-8cfd-6d7c091b76bd)
 Call ID: 2d68688f-168f-4d9f-8cfd-6d7c091b76bd
  Args:
    target: Ernest_Augustus_Crown_Prince_of_Hanover
    source: Princess_Marie_Louise_of_Hanover_and_Cumberland
    relation: :hasFather
  AddTriple (1601ba79-673d-40f4-9700-2bbe07f1c945)
 Call ID: 1601ba79-673d-40f4-9700-2bbe07f1c945
  Args:
    relation: :hasRelation
    source: Princess_Marie_Alexandra_of_Baden
    target: Prince_Wolfgang_of_Hesse
  Finish (f2f34ba1-7733-433f-b5d8-58769b804932)
 Call ID: f2f34ba1-7733-433f-b5d8-58769b804932
  Args: