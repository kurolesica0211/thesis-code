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
Queen Margrethe II


Countess Athena of Monpezat (born Athena Marguerite Françoise Marie; 24 January 2012) is a member of the Danish royal family.
She is the younger child and only daughter of Prince Joachim and Princess Marie of Denmark.
She is the youngest grandchild of Queen Margrethe II and Prince Henrik, and the niece of King Frederik X. Athena is currently ninth in the line of succession to the Danish throne.
Biography

Athena was born a princess of Denmark on 24 January 2012 at Rigshospitalet, the Copenhagen University Hospital.
She has two older half-brothers from her father's first marriage, Nikolai and Felix, and an older brother, Henrik.
In accordance with Danish royal traditions, her names were not revealed until her christening, which took place on 20 May 2012 at the Møgeltønder Church, where her older brothers Felix and Henrik were also christened.
She was named Athena Marguerite Françoise Marie for both of her grandmothers as well as for her mother.
Her godparents are her maternal uncles, Gregory Grandet and Edouard Cavallier; Carina Axelsson, the long-term girlfriend of her father's cousin Gustav, Hereditary Prince of Sayn-Wittgenstein-Berleburg; and friends of her parents, Julie Mirabaud, Diego de Lavandeyra and Henriette Steenstrup.
Joseph Søstrenes Skole – the same Catholic private school in Ordrup as her brother Henrik.
In 2019, when Athena and her family moved to France, she was enrolled at the private school EIB Monceau in the 8th arrondissement of Paris alongside her brother.
Titles and styles

Athena was styled as "Her Highness Princess Athena of Denmark, Countess of Monpezat" from birth until 1 January 2023.
In September 2022, Queen Margrethe II decided to restrict the titles Prince and Princess to the direct line of succession to the throne.
Since 1 January 2023, she has been known as "Her Excellency Countess Athena of Monpezat".



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
  AssignClass (d39d882c-9503-4213-aaf5-153d787b8cf3)
 Call ID: d39d882c-9503-4213-aaf5-153d787b8cf3
  Args:
    type: :Woman
    source: Athena_of_Monpezat
  AssignClass (7fb0d4b2-ef83-4064-b34a-bf14bd8955f4)
 Call ID: 7fb0d4b2-ef83-4064-b34a-bf14bd8955f4
  Args:
    source: Athena_of_Monpezat
    type: :Person
  AddLiteral (61c59caf-ab2c-4fdd-83d1-7096cbe99f26)
 Call ID: 61c59caf-ab2c-4fdd-83d1-7096cbe99f26
  Args:
    source: Athena_of_Monpezat
    relation: :knownAs
    literal_type: xsd:string
    literal_value: Athena Marguerite Françoise Marie
  AddLiteral (ce25f0b3-b594-4ba7-91ab-c4986c2cbc0c)
 Call ID: ce25f0b3-b594-4ba7-91ab-c4986c2cbc0c
  Args:
    source: Athena_of_Monpezat
    relation: :hasBirthYear
    literal_value: 2012
    literal_type: xsd:integer
  AssignClass (bb3d8f1b-86e3-4b87-adf5-279f25c57ded)
 Call ID: bb3d8f1b-86e3-4b87-adf5-279f25c57ded
  Args:
    source: Joachim_of_Denmark
    type: :Man
  AssignClass (8525590e-9736-4c2b-b32f-7608cdaeeb0d)
 Call ID: 8525590e-9736-4c2b-b32f-7608cdaeeb0d
  Args:
    type: :Person
    source: Joachim_of_Denmark
  AssignClass (86ddfbf3-268d-4ee1-b73c-605272d29766)
 Call ID: 86ddfbf3-268d-4ee1-b73c-605272d29766
  Args:
    type: :Woman
    source: Marie_of_Denmark
  AssignClass (f2001085-4cd1-4654-84fb-6e35d9a9202d)
 Call ID: f2001085-4cd1-4654-84fb-6e35d9a9202d
  Args:
    source: Marie_of_Denmark
    type: :Person
  AddTriple (3918f469-e25b-4b37-8094-ebf16901b611)
 Call ID: 3918f469-e25b-4b37-8094-ebf16901b611
  Args:
    target: Joachim_of_Denmark
    source: Athena_of_Monpezat
    relation: :hasFather
  AddTriple (cddc97ac-0bf3-4d93-9c16-015eda322381)
 Call ID: cddc97ac-0bf3-4d93-9c16-015eda322381
  Args:
    relation: :hasMother
    source: Athena_of_Monpezat
    target: Marie_of_Denmark
  AssignClass (f6a6a9de-25c3-4fa2-bfb7-5a0d607a3ab8)
 Call ID: f6a6a9de-25c3-4fa2-bfb7-5a0d607a3ab8
  Args:
    type: :Woman
    source: Margrethe_II
  AssignClass (3761d08a-0ded-4241-ba59-a51dee44caa8)
 Call ID: 3761d08a-0ded-4241-ba59-a51dee44caa8
  Args:
    type: :Person
    source: Margrethe_II
  AssignClass (d6dedff8-6268-425a-9234-25114bcb896a)
 Call ID: d6dedff8-6268-425a-9234-25114bcb896a
  Args:
    type: :Man
    source: Henrik_of_Denmark
  AssignClass (93b6f78c-3444-4615-ad52-926f901b79a0)
 Call ID: 93b6f78c-3444-4615-ad52-926f901b79a0
  Args:
    type: :Person
    source: Henrik_of_Denmark
  AddTriple (f643da80-6158-4e17-b28c-4c15df1afcea)
 Call ID: f643da80-6158-4e17-b28c-4c15df1afcea
  Args:
    target: Margrethe_II
    source: Joachim_of_Denmark
    relation: :hasParent
  AddTriple (7a9abf73-a39b-494d-87c3-5ac4f8f69d21)
 Call ID: 7a9abf73-a39b-494d-87c3-5ac4f8f69d21
  Args:
    target: Henrik_of_Denmark
    relation: :hasParent
    source: Joachim_of_Denmark
  AssignClass (dfda3fbd-86f3-4df7-9dde-7c3dc05945c5)
 Call ID: dfda3fbd-86f3-4df7-9dde-7c3dc05945c5
  Args:
    source: Frederik_X
    type: :Man
  AssignClass (cb4c323b-ac01-431e-8386-f859c5bc84c1)
 Call ID: cb4c323b-ac01-431e-8386-f859c5bc84c1
  Args:
    source: Frederik_X
    type: :Person
  AssignClass (6ae0073b-9aa0-4931-85f1-b6991d8c8d26)
 Call ID: 6ae0073b-9aa0-4931-85f1-b6991d8c8d26
  Args:
    type: :Man
    source: Nikolai_of_Denmark
  AssignClass (620521e2-5491-4f57-afb8-e4c0ca8e8885)
 Call ID: 620521e2-5491-4f57-afb8-e4c0ca8e8885
  Args:
    type: :Person
    source: Nikolai_of_Denmark
  AssignClass (9227cee0-11ce-4444-8f90-0923ec21ba99)
 Call ID: 9227cee0-11ce-4444-8f90-0923ec21ba99
  Args:
    source: Felix_of_Denmark
    type: :Man
  AssignClass (4ee844af-57c9-4df1-aa73-b591711216cd)
 Call ID: 4ee844af-57c9-4df1-aa73-b591711216cd
  Args:
    type: :Person
    source: Felix_of_Denmark
  AssignClass (e4ecf388-5b22-4fbf-bf42-a2994226d2aa)
 Call ID: e4ecf388-5b22-4fbf-bf42-a2994226d2aa
  Args:
    source: Henrik_of_Monpezat
    type: :Man
  AssignClass (5d704963-517a-4503-93b5-587e4903d2af)
 Call ID: 5d704963-517a-4503-93b5-587e4903d2af
  Args:
    source: Henrik_of_Monpezat
    type: :Person
  AddTriple (8566a03c-59d1-4e08-9604-125b5ad71243)
 Call ID: 8566a03c-59d1-4e08-9604-125b5ad71243
  Args:
    source: Henrik_of_Monpezat
    relation: :isBrotherOf
    target: Athena_of_Monpezat
  AddTriple (72e28fd8-5482-4930-ab63-37cd911e23dc)
 Call ID: 72e28fd8-5482-4930-ab63-37cd911e23dc
  Args:
    relation: :isFatherOf
    source: Joachim_of_Denmark
    target: Nikolai_of_Denmark
  AddTriple (cb171916-ac7b-4af9-84a7-6532fb745372)
 Call ID: cb171916-ac7b-4af9-84a7-6532fb745372
  Args:
    target: Felix_of_Denmark
    relation: :isFatherOf
    source: Joachim_of_Denmark
  AddTriple (89031f3f-2097-43f2-8e25-2ee7ffcb1465)
 Call ID: 89031f3f-2097-43f2-8e25-2ee7ffcb1465
  Args:
    target: Henrik_of_Monpezat
    source: Joachim_of_Denmark
    relation: :isFatherOf
  Finish (1fb40822-7bc8-4a93-9b78-25927b53d4e2)
 Call ID: 1fb40822-7bc8-4a93-9b78-25927b53d4e2
  Args: