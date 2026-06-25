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
Victoria Federica de Todos los Santos de Marichalar y Borbón, Lady of Tejada GE (born 9 September 2000) is the younger child and only daughter of Infanta Elena, Duchess of Lugo, and Jaime de Marichalar.
She is a granddaughter of King Juan Carlos I and Queen Sofía of Spain and a niece of King Felipe VI.
Victoria is fifth in the line of succession to the Spanish throne after her cousins, King Felipe's daughters Leonor, Princess of Asturias, and Infanta Sofía; her mother; and her brother, Felipe.
Early life and education

Victoria de Marichalar y Borbón was born 9 September 2000 at 13:00 in Ruber International Hospital in Madrid.
She made her first Holy Communion on 27 May 2009 at the Dominicos Church in Alcobendas, Spain.
Then she studied at a British boarding school for 3 years before returning to Spain at St. George's de La Moraleja.
Victoria studied ballet and horse riding.
Career

Marichalar has been reported to be working in the fashion industry and is quoted as saying that fashion is her "true calling".



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
  AssignClass (0b22e9af-d431-4161-808f-986eee084115)
 Call ID: 0b22e9af-d431-4161-808f-986eee084115
  Args:
    type: :Person
    source: :Victoria_Federica_de_Marichalar_y_Borbon
  AssignClass (e95f5f22-cbb9-4836-84c2-6f0ddf6abeae)
 Call ID: e95f5f22-cbb9-4836-84c2-6f0ddf6abeae
  Args:
    type: :Woman
    source: :Victoria_Federica_de_Marichalar_y_Borbon
  AssignClass (65ff5e18-ebd3-453b-8dde-e7462e1ad40c)
 Call ID: 65ff5e18-ebd3-453b-8dde-e7462e1ad40c
  Args:
    type: :Person
    source: :Infanta_Elena
  AssignClass (198fbaf7-a1b6-4186-baaf-f5ca43be0ddc)
 Call ID: 198fbaf7-a1b6-4186-baaf-f5ca43be0ddc
  Args:
    source: :Infanta_Elena
    type: :Woman
  AssignClass (922f89a3-e1e3-4fcb-8d3c-7446761b439e)
 Call ID: 922f89a3-e1e3-4fcb-8d3c-7446761b439e
  Args:
    type: :Person
    source: :Jaime_de_Marichalar
  AssignClass (835553d1-c376-440f-8af5-7e7e5b046807)
 Call ID: 835553d1-c376-440f-8af5-7e7e5b046807
  Args:
    source: :Jaime_de_Marichalar
    type: :Man
  AddLiteral (539b4a5a-0483-4205-9a70-785b39521c9f)
 Call ID: 539b4a5a-0483-4205-9a70-785b39521c9f
  Args:
    source: :Victoria_Federica_de_Marichalar_y_Borbon
    literal_type: xsd:integer
    literal_value: 2000
    relation: :hasBirthYear
  AddTriple (9bb22cb7-17d4-4087-a48b-0335a3d1795a)
 Call ID: 9bb22cb7-17d4-4087-a48b-0335a3d1795a
  Args:
    relation: :hasMother
    target: :Infanta_Elena
    source: :Victoria_Federica_de_Marichalar_y_Borbon
  AddTriple (6b8e6c92-4c7a-41f4-8def-9de784fe4266)
 Call ID: 6b8e6c92-4c7a-41f4-8def-9de784fe4266
  Args:
    target: :Jaime_de_Marichalar
    source: :Victoria_Federica_de_Marichalar_y_Borbon
    relation: :hasFather
  AssignClass (3794f412-dee6-420a-87b2-da760b83eedd)
 Call ID: 3794f412-dee6-420a-87b2-da760b83eedd
  Args:
    type: :Person
    source: :Juan_Carlos_I
  AssignClass (a166e6a4-42b0-43c4-845d-a716587eebfb)
 Call ID: a166e6a4-42b0-43c4-845d-a716587eebfb
  Args:
    source: :Juan_Carlos_I
    type: :Man
  AssignClass (10630411-0e94-4b52-bd69-7d5e58678c0d)
 Call ID: 10630411-0e94-4b52-bd69-7d5e58678c0d
  Args:
    source: :Sofia_of_Spain
    type: :Person
  AssignClass (77b97a25-7be0-4646-8ba0-8ca105448426)
 Call ID: 77b97a25-7be0-4646-8ba0-8ca105448426
  Args:
    source: :Sofia_of_Spain
    type: :Woman
  AddTriple (5cb702ee-5057-4ecc-9ed3-b87d9d4cea75)
 Call ID: 5cb702ee-5057-4ecc-9ed3-b87d9d4cea75
  Args:
    target: :Juan_Carlos_I
    source: :Infanta_Elena
    relation: :hasParent
  AddTriple (751ec7e7-e6fa-4891-ad25-9ec06cab9b7a)
 Call ID: 751ec7e7-e6fa-4891-ad25-9ec06cab9b7a
  Args:
    source: :Infanta_Elena
    target: :Sofia_of_Spain
    relation: :hasParent
  AssignClass (78a53ef0-8f2b-44c9-bfaf-b68149f99a12)
 Call ID: 78a53ef0-8f2b-44c9-bfaf-b68149f99a12
  Args:
    source: :Felipe_VI
    type: :Person
  AssignClass (70e001b0-ddc0-479f-bf00-8fdacbe265d5)
 Call ID: 70e001b0-ddc0-479f-bf00-8fdacbe265d5
  Args:
    type: :Man
    source: :Felipe_VI
  AssignClass (99cac6a3-d52e-458f-bc29-90be778dd983)
 Call ID: 99cac6a3-d52e-458f-bc29-90be778dd983
  Args:
    source: :Felipe_de_Marichalar
    type: :Person
  AssignClass (f2f0e17e-1133-467e-97dd-ccc50bc410cb)
 Call ID: f2f0e17e-1133-467e-97dd-ccc50bc410cb
  Args:
    source: :Felipe_de_Marichalar
    type: :Man
  AddTriple (ab917656-c8de-448c-b6b0-87480efbc6ec)
 Call ID: ab917656-c8de-448c-b6b0-87480efbc6ec
  Args:
    relation: :hasBrother
    source: :Victoria_Federica_de_Marichalar_y_Borbon
    target: :Felipe_de_Marichalar
  AssignClass (ffb0d448-1450-494b-8c47-1c621710b2fe)
 Call ID: ffb0d448-1450-494b-8c47-1c621710b2fe
  Args:
    source: :Leonor_Princess_of_Asturias
    type: :Person
  AssignClass (5fdf4ed3-ee2c-47f0-8e95-a2c659b75280)
 Call ID: 5fdf4ed3-ee2c-47f0-8e95-a2c659b75280
  Args:
    type: :Woman
    source: :Leonor_Princess_of_Asturias
  AssignClass (17034b34-68b5-4505-9588-7a2ea525a8fc)
 Call ID: 17034b34-68b5-4505-9588-7a2ea525a8fc
  Args:
    source: :Infanta_Sofia
    type: :Person
  AssignClass (1ba66bd6-ac0a-499c-b830-71cc34fa9201)
 Call ID: 1ba66bd6-ac0a-499c-b830-71cc34fa9201
  Args:
    type: :Woman
    source: :Infanta_Sofia
  AddTriple (061fbaa3-e499-4819-acf9-f77e27991b98)
 Call ID: 061fbaa3-e499-4819-acf9-f77e27991b98
  Args:
    source: :Leonor_Princess_of_Asturias
    target: :Felipe_VI
    relation: :hasParent
  AddTriple (035fd633-25e1-48aa-902c-a5122e1f771d)
 Call ID: 035fd633-25e1-48aa-902c-a5122e1f771d
  Args:
    source: :Infanta_Sofia
    target: :Felipe_VI
    relation: :hasParent
  Finish (df46208a-e6d4-4fbe-8658-4d81286bce96)
 Call ID: df46208a-e6d4-4fbe-8658-4d81286bce96
  Args: