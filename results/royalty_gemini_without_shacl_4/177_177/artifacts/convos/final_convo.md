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
Princess Elisabeth of Denmark (Elisabeth Caroline-Mathilde Alexandrine Helena Olga Thyra Feodora Estrid Margrethe Désirée; 8 May 1935 – 19 June 2018) was a member of the Danish royal family.
The only daughter and eldest child of Knud, Hereditary Prince of Denmark, and Princess Caroline-Mathilde of Denmark, she was a granddaughter of Christian X, niece of Frederik IX, and first cousin of Margrethe II.
In addition to undertaking occasionally royal duties, she was a career diplomat with the Ministry of Foreign Affairs of Denmark.
Early life and education

Elisabeth was born on 8 May 1935 in Copenhagen to Prince Knud and Princess Caroline-Mathilde of Denmark.
Her father was the second son of Christian X.
The family resided at Sorgenfri Palace in Kongens Lyngby, where she was raised with her two younger brothers Prince Ingolf and Prince Christian.
During the 1938-39 Mørkefjord expedition, paleontologist Eigil Nielsen named the Princess Elisabeth Alps in northeastern Greenland after her.
Elisabeth began her education privately at Sorgenfri.
In 1953, when  succession to the Danish throne switched from agnatic primogeniture to male-preference primogeniture, Elisabeth gained succession rights and became seventh in line to the throne.
She was titled of Prinsesse til Danmark (literally translated as "Princess to Denmark", reserved for members of the Royal Family in the line of succession) with the style of Highness.
She was the only one of her siblings to retain her title and succession rights, as her younger brothers married commoners without the permission of their uncle, Frederik IX.
Career

In 1956, Elisabeth began her career with the Danish Ministry of Foreign Affairs.
She was posted to the Embassy of Denmark, Washington, D.C. from 1973 to 1976 and again from 1981 to 1985.
In addition to her diplomatic career, Elisabeth occasionally undertook royal duties on behalf of her uncle and later cousin.
Personal life and death

Elisabeth never married nor had children.
After a long period of ill health, Elisabeth died on 19 June 2018, at the age of 83.



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
  AssignClass (593403d2-12e3-4cc8-8ff7-cef4a4448477)
 Call ID: 593403d2-12e3-4cc8-8ff7-cef4a4448477
  Args:
    type: :Woman
    source: Princess_Elisabeth_of_Denmark
  AssignClass (1a3e9fde-2691-49dd-a875-5edf0420836d)
 Call ID: 1a3e9fde-2691-49dd-a875-5edf0420836d
  Args:
    type: :Person
    source: Princess_Elisabeth_of_Denmark
  AddLiteral (609d0d20-884d-418c-87cc-c9c93b76f4aa)
 Call ID: 609d0d20-884d-418c-87cc-c9c93b76f4aa
  Args:
    literal_value: 1935
    relation: :hasBirthYear
    source: Princess_Elisabeth_of_Denmark
    literal_type: xsd:nonNegativeInteger
  AddLiteral (9419bdcb-0fe7-460e-9d73-5ffc7ff739a5)
 Call ID: 9419bdcb-0fe7-460e-9d73-5ffc7ff739a5
  Args:
    relation: :hasDeathYear
    literal_value: 2018
    literal_type: xsd:nonNegativeInteger
    source: Princess_Elisabeth_of_Denmark
  AssignClass (de237ff4-ab3c-46c8-90ca-5c826b8ffd88)
 Call ID: de237ff4-ab3c-46c8-90ca-5c826b8ffd88
  Args:
    type: :Man
    source: Knud_Hereditary_Prince_of_Denmark
  AssignClass (9e144f32-d1e2-4de9-9040-6b686040eeec)
 Call ID: 9e144f32-d1e2-4de9-9040-6b686040eeec
  Args:
    type: :Person
    source: Knud_Hereditary_Prince_of_Denmark
  AssignClass (28a23112-de78-4588-ae74-84c8546fdb83)
 Call ID: 28a23112-de78-4588-ae74-84c8546fdb83
  Args:
    type: :Woman
    source: Princess_Caroline-Mathilde_of_Denmark
  AssignClass (05dbfbbf-0d47-40b0-aef1-8aa10a9c67a9)
 Call ID: 05dbfbbf-0d47-40b0-aef1-8aa10a9c67a9
  Args:
    type: :Person
    source: Princess_Caroline-Mathilde_of_Denmark
  AddTriple (05a097f3-0f2f-43a9-8174-2a217a6cbd96)
 Call ID: 05a097f3-0f2f-43a9-8174-2a217a6cbd96
  Args:
    target: Knud_Hereditary_Prince_of_Denmark
    source: Princess_Elisabeth_of_Denmark
    relation: :hasFather
  AddTriple (b0301970-38b6-4886-b933-ea637063587e)
 Call ID: b0301970-38b6-4886-b933-ea637063587e
  Args:
    source: Princess_Elisabeth_of_Denmark
    target: Princess_Caroline-Mathilde_of_Denmark
    relation: :hasMother
  AssignClass (318ce61d-4ad0-48ef-99f9-1b4476cf98c8)
 Call ID: 318ce61d-4ad0-48ef-99f9-1b4476cf98c8
  Args:
    type: :Man
    source: Christian_X
  AssignClass (c22e2086-d1af-4e23-b71e-4efa0603a4ad)
 Call ID: c22e2086-d1af-4e23-b71e-4efa0603a4ad
  Args:
    type: :Person
    source: Christian_X
  AddTriple (c6ee346a-ad1c-4724-b71f-1185933c98bd)
 Call ID: c6ee346a-ad1c-4724-b71f-1185933c98bd
  Args:
    relation: :hasFather
    target: Christian_X
    source: Knud_Hereditary_Prince_of_Denmark
  AssignClass (e6894726-db68-4aeb-9f05-2c448dfd2946)
 Call ID: e6894726-db68-4aeb-9f05-2c448dfd2946
  Args:
    type: :Man
    source: Frederik_IX
  AssignClass (6a03ea85-0507-4193-9608-36836d5ebac1)
 Call ID: 6a03ea85-0507-4193-9608-36836d5ebac1
  Args:
    type: :Person
    source: Frederik_IX
  AssignClass (b5013b17-e3a4-4d00-ad1c-5856bb351405)
 Call ID: b5013b17-e3a4-4d00-ad1c-5856bb351405
  Args:
    type: :Woman
    source: Margrethe_II
  AssignClass (dc8d42fd-6810-4d1a-9c64-ecf07eb2f062)
 Call ID: dc8d42fd-6810-4d1a-9c64-ecf07eb2f062
  Args:
    type: :Person
    source: Margrethe_II
  AssignClass (0012f85a-1309-4a79-b82f-53cc3a8d1bf7)
 Call ID: 0012f85a-1309-4a79-b82f-53cc3a8d1bf7
  Args:
    type: :Man
    source: Prince_Ingolf
  AssignClass (bc043656-c07a-4991-a7aa-dd0377fcf1fd)
 Call ID: bc043656-c07a-4991-a7aa-dd0377fcf1fd
  Args:
    type: :Person
    source: Prince_Ingolf
  AssignClass (f46c798e-cd9e-4143-9b1d-65974c66f83e)
 Call ID: f46c798e-cd9e-4143-9b1d-65974c66f83e
  Args:
    type: :Man
    source: Prince_Christian
  AssignClass (39c1e54d-9275-4002-b34e-508809d530a2)
 Call ID: 39c1e54d-9275-4002-b34e-508809d530a2
  Args:
    type: :Person
    source: Prince_Christian
  AddTriple (6a0c4210-f26d-4fdf-8932-4a0a2569a50b)
 Call ID: 6a0c4210-f26d-4fdf-8932-4a0a2569a50b
  Args:
    relation: :hasBrother
    source: Princess_Elisabeth_of_Denmark
    target: Prince_Ingolf
  AddTriple (89dd63ee-1769-43e2-862c-b34bc640141e)
 Call ID: 89dd63ee-1769-43e2-862c-b34bc640141e
  Args:
    relation: :hasBrother
    source: Princess_Elisabeth_of_Denmark
    target: Prince_Christian
  Finish (c28d13eb-abf2-48b6-9e59-aab502ab98de)
 Call ID: c28d13eb-abf2-48b6-9e59-aab502ab98de
  Args: