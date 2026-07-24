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
  AssignClass (e44d7c31-7392-495e-ac2d-59f6f4e68c22)
 Call ID: e44d7c31-7392-495e-ac2d-59f6f4e68c22
  Args:
    type: :Woman
    source: Marie_Alexandra_of_Baden
  AddLiteral (5ec855e7-6cf3-4b72-944d-2b408ed30a96)
 Call ID: 5ec855e7-6cf3-4b72-944d-2b408ed30a96
  Args:
    relation: :hasBirthYear
    literal_value: 1902
    source: Marie_Alexandra_of_Baden
    literal_type: xsd:integer
  AddLiteral (1992c152-085e-440c-9d07-dc684862f4c9)
 Call ID: 1992c152-085e-440c-9d07-dc684862f4c9
  Args:
    literal_type: xsd:integer
    source: Marie_Alexandra_of_Baden
    literal_value: 1944
    relation: :hasDeathYear
  AssignClass (5b54106a-e470-4564-baab-409df1df7346)
 Call ID: 5b54106a-e470-4564-baab-409df1df7346
  Args:
    type: :Man
    source: Prince_Maximilian_of_Baden
  AddLiteral (aaedb220-b9e3-49ee-963c-118e20368301)
 Call ID: aaedb220-b9e3-49ee-963c-118e20368301
  Args:
    source: Prince_Maximilian_of_Baden
    literal_value: 1867
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (ce1a099a-2870-4b14-8114-703a6bdc7ec2)
 Call ID: ce1a099a-2870-4b14-8114-703a6bdc7ec2
  Args:
    literal_type: xsd:integer
    source: Prince_Maximilian_of_Baden
    literal_value: 1929
    relation: :hasDeathYear
  AssignClass (8265af15-4ad5-4901-95fa-ff36a21d511f)
 Call ID: 8265af15-4ad5-4901-95fa-ff36a21d511f
  Args:
    source: Princess_Marie_Louise_of_Hanover_and_Cumberland
    type: :Woman
  AddLiteral (a36836ad-b542-4322-affd-9d72da4ccccc)
 Call ID: a36836ad-b542-4322-affd-9d72da4ccccc
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1879
    source: Princess_Marie_Louise_of_Hanover_and_Cumberland
  AddLiteral (3a395a47-33e7-45be-bc2f-a8266b254051)
 Call ID: 3a395a47-33e7-45be-bc2f-a8266b254051
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Princess_Marie_Louise_of_Hanover_and_Cumberland
    literal_value: 1948
  AddTriple (d6d608b5-46a8-41ed-a5c2-4d4de21e8c9b)
 Call ID: d6d608b5-46a8-41ed-a5c2-4d4de21e8c9b
  Args:
    target: Prince_Maximilian_of_Baden
    source: Marie_Alexandra_of_Baden
    relation: :hasFather
  AddTriple (625d0461-2e4c-4547-bec6-074df14793ed)
 Call ID: 625d0461-2e4c-4547-bec6-074df14793ed
  Args:
    relation: :hasMother
    target: Princess_Marie_Louise_of_Hanover_and_Cumberland
    source: Marie_Alexandra_of_Baden
  AssignClass (3db4fea8-5673-494d-9338-bd96e74dc470)
 Call ID: 3db4fea8-5673-494d-9338-bd96e74dc470
  Args:
    type: :Man
    source: Prince_Wilhelm_of_Baden
  AddLiteral (d04a6e86-083b-42da-bf06-9e8623275b19)
 Call ID: d04a6e86-083b-42da-bf06-9e8623275b19
  Args:
    source: Prince_Wilhelm_of_Baden
    literal_value: 1829
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (5500daf2-b151-4c08-b598-48b7cf7d06ec)
 Call ID: 5500daf2-b151-4c08-b598-48b7cf7d06ec
  Args:
    relation: :hasDeathYear
    literal_value: 1897
    source: Prince_Wilhelm_of_Baden
    literal_type: xsd:integer
  AssignClass (982998b6-1c1a-4ceb-a4a9-6fc9e11e0705)
 Call ID: 982998b6-1c1a-4ceb-a4a9-6fc9e11e0705
  Args:
    type: :Woman
    source: Princess_Maria_Maximilianovna_of_Leuchtenberg
  AddLiteral (a61e0eeb-a838-49fc-8249-e14af72591e7)
 Call ID: a61e0eeb-a838-49fc-8249-e14af72591e7
  Args:
    source: Princess_Maria_Maximilianovna_of_Leuchtenberg
    literal_value: 1841
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (bc5e4a37-abbe-426d-9e31-7420f6802080)
 Call ID: bc5e4a37-abbe-426d-9e31-7420f6802080
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1914
    source: Princess_Maria_Maximilianovna_of_Leuchtenberg
  AddTriple (6c2da9b1-ddeb-4d70-aebe-59094b6dec16)
 Call ID: 6c2da9b1-ddeb-4d70-aebe-59094b6dec16
  Args:
    relation: :hasFather
    source: Prince_Maximilian_of_Baden
    target: Prince_Wilhelm_of_Baden
  AddTriple (976e6d58-9899-44d3-b141-15bf872cda2a)
 Call ID: 976e6d58-9899-44d3-b141-15bf872cda2a
  Args:
    relation: :hasMother
    target: Princess_Maria_Maximilianovna_of_Leuchtenberg
    source: Prince_Maximilian_of_Baden
  AssignClass (c972f279-6fab-4068-8e85-389c2004c502)
 Call ID: c972f279-6fab-4068-8e85-389c2004c502
  Args:
    type: :Man
    source: Maximilian_Duke_of_Leuchtenberg
  AddLiteral (5508c275-a2ec-4899-876f-b7b52b0e6584)
 Call ID: 5508c275-a2ec-4899-876f-b7b52b0e6584
  Args:
    literal_type: xsd:integer
    source: Maximilian_Duke_of_Leuchtenberg
    literal_value: 1817
    relation: :hasBirthYear
  AddLiteral (9e689959-dbb5-4bf6-b971-0b02cc90f148)
 Call ID: 9e689959-dbb5-4bf6-b971-0b02cc90f148
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1852
    source: Maximilian_Duke_of_Leuchtenberg
  AssignClass (1286c50d-f169-43fa-a014-dead436100f6)
 Call ID: 1286c50d-f169-43fa-a014-dead436100f6
  Args:
    source: Grand_Duchess_Maria_Nikolaevna
    type: :Woman
  AddLiteral (3f512d3d-1157-4a66-9152-b5699d4c48b4)
 Call ID: 3f512d3d-1157-4a66-9152-b5699d4c48b4
  Args:
    relation: :hasBirthYear
    source: Grand_Duchess_Maria_Nikolaevna
    literal_value: 1819
    literal_type: xsd:integer
  AddLiteral (e770c6e3-432f-4ae6-8d13-7e3b56d95d81)
 Call ID: e770c6e3-432f-4ae6-8d13-7e3b56d95d81
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1876
    source: Grand_Duchess_Maria_Nikolaevna
  AddTriple (d6500b72-40d5-4a40-aa2f-5169ff52fe44)
 Call ID: d6500b72-40d5-4a40-aa2f-5169ff52fe44
  Args:
    relation: :hasFather
    source: Princess_Maria_Maximilianovna_of_Leuchtenberg
    target: Maximilian_Duke_of_Leuchtenberg
  AddTriple (eedace7c-d1ab-4d5f-9f29-b992c60e83ec)
 Call ID: eedace7c-d1ab-4d5f-9f29-b992c60e83ec
  Args:
    relation: :hasMother
    target: Grand_Duchess_Maria_Nikolaevna
    source: Princess_Maria_Maximilianovna_of_Leuchtenberg
  AssignClass (eaaaa3ff-fc88-4127-8dba-361862b1d80b)
 Call ID: eaaaa3ff-fc88-4127-8dba-361862b1d80b
  Args:
    source: Ernest_Augustus_Crown_Prince_of_Hanover
    type: :Man
  AddTriple (e33b2241-c541-4df4-a057-a18381ec2050)
 Call ID: e33b2241-c541-4df4-a057-a18381ec2050
  Args:
    source: Princess_Marie_Louise_of_Hanover_and_Cumberland
    target: Ernest_Augustus_Crown_Prince_of_Hanover
    relation: :hasFather
  AssignClass (988c754a-c521-4c9c-bdf6-a02357111a78)
 Call ID: 988c754a-c521-4c9c-bdf6-a02357111a78
  Args:
    type: :Man
    source: Prince_Wolfgang_of_Hesse
  AddLiteral (d3a1e6b2-df66-4ff1-8857-62ef23f433ff)
 Call ID: d3a1e6b2-df66-4ff1-8857-62ef23f433ff
  Args:
    literal_value: 1896
    source: Prince_Wolfgang_of_Hesse
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (4a4e2f2f-b416-431f-9d59-9237862aa713)
 Call ID: 4a4e2f2f-b416-431f-9d59-9237862aa713
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Prince_Wolfgang_of_Hesse
    literal_value: 1989
  AddLiteral (3b34e96e-18f4-4b91-aefc-4203ec8ff1e5)
 Call ID: 3b34e96e-18f4-4b91-aefc-4203ec8ff1e5
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1924
    source: Marie_Alexandra_of_Baden
  AddTriple (87ec1381-658e-43b9-97e0-2d27051cef99)
 Call ID: 87ec1381-658e-43b9-97e0-2d27051cef99
  Args:
    relation: :hasRelation
    target: Prince_Wolfgang_of_Hesse
    source: Marie_Alexandra_of_Baden
  Finish (1bc349c3-1cde-49d8-abcd-eabb1b8c46aa)
 Call ID: 1bc349c3-1cde-49d8-abcd-eabb1b8c46aa
  Args: