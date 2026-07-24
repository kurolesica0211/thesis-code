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
Klaus Felix von Amsberg (German: Klaus Felix Friedrich Leopold Gabriel Archim Julius August von Amsberg; 1 September 1890 – 19 December 1953) was a member of the German Niederer Adel (lower nobility) and father of Prince Claus of the Netherlands.
Early life

He was born at Rehna, Mecklenburg-Schwerin, German Empire (now Mecklenburg-Vorpommern, Germany), the first child of Wilhelm von Amsberg (1856–1929), by his marriage to Elise von Vieregg (1866–1951), member of an old aristocratic family.
Claus was from 1917 the steward of an estate after a failed venture in Africa as a planter.
Marriage

Claus married on 4 September 1924 at Hitzacker to Baroness Gösta von dem Bussche-Haddenhausen (26 January 1902 –
13 June 1996), daughter of Baron Georg von dem Bussche-Haddenhausen (1869–1923) and Baroness Gabriele von dem Bussche-Ippenburg (1877–1973).



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
  AssignClass (91c587d0-a1d1-40bf-8d7c-74eb049c8f89)
 Call ID: 91c587d0-a1d1-40bf-8d7c-74eb049c8f89
  Args:
    type: :Man
    source: Klaus_Felix_von_Amsberg
  AddLiteral (9ece50b0-cef3-4467-98ad-952a13bfa151)
 Call ID: 9ece50b0-cef3-4467-98ad-952a13bfa151
  Args:
    literal_type: xsd:integer
    literal_value: 1890
    source: Klaus_Felix_von_Amsberg
    relation: :hasBirthYear
  AddLiteral (19d5d4c6-096a-4700-96e6-833b037a9448)
 Call ID: 19d5d4c6-096a-4700-96e6-833b037a9448
  Args:
    source: Klaus_Felix_von_Amsberg
    literal_value: 1953
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (b1203e9f-464b-4900-8c6d-e1f4b85cbf4a)
 Call ID: b1203e9f-464b-4900-8c6d-e1f4b85cbf4a
  Args:
    type: :Man
    source: Wilhelm_von_Amsberg
  AddLiteral (5527c06b-01fb-4ed8-b6eb-ef94fc0533b6)
 Call ID: 5527c06b-01fb-4ed8-b6eb-ef94fc0533b6
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1856
    source: Wilhelm_von_Amsberg
  AddLiteral (a38fbc8b-3bcd-4d42-bcb3-6331a9c99b96)
 Call ID: a38fbc8b-3bcd-4d42-bcb3-6331a9c99b96
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1929
    source: Wilhelm_von_Amsberg
  AssignClass (074ead92-de8f-457a-9fe8-335c9611ef1b)
 Call ID: 074ead92-de8f-457a-9fe8-335c9611ef1b
  Args:
    type: :Woman
    source: Elise_von_Vieregg
  AddLiteral (e3616b55-3923-4f9c-a22f-e4f6b98b36d3)
 Call ID: e3616b55-3923-4f9c-a22f-e4f6b98b36d3
  Args:
    relation: :hasBirthYear
    source: Elise_von_Vieregg
    literal_value: 1866
    literal_type: xsd:integer
  AddLiteral (6c5b40a2-9c0a-4ecf-8812-bc6cf979d714)
 Call ID: 6c5b40a2-9c0a-4ecf-8812-bc6cf979d714
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1951
    source: Elise_von_Vieregg
  AddTriple (8b78f329-525d-41ff-b995-c7ee4511016c)
 Call ID: 8b78f329-525d-41ff-b995-c7ee4511016c
  Args:
    target: Wilhelm_von_Amsberg
    source: Klaus_Felix_von_Amsberg
    relation: :hasFather
  AddTriple (e992e5c7-1ca8-40b2-a144-c6d9d8b247af)
 Call ID: e992e5c7-1ca8-40b2-a144-c6d9d8b247af
  Args:
    relation: :hasMother
    source: Klaus_Felix_von_Amsberg
    target: Elise_von_Vieregg
  AssignClass (b16453ce-4efc-4044-94d7-ae0887fe1698)
 Call ID: b16453ce-4efc-4044-94d7-ae0887fe1698
  Args:
    type: :Woman
    source: Gosta_von_dem_Bussche-Haddenhausen
  AddLiteral (46fc4075-caaf-4b06-8e35-9bd9ce7e1101)
 Call ID: 46fc4075-caaf-4b06-8e35-9bd9ce7e1101
  Args:
    relation: :hasBirthYear
    literal_value: 1902
    source: Gosta_von_dem_Bussche-Haddenhausen
    literal_type: xsd:integer
  AddLiteral (d35f63c8-4c66-497e-a65f-1ba160f2904a)
 Call ID: d35f63c8-4c66-497e-a65f-1ba160f2904a
  Args:
    relation: :hasDeathYear
    source: Gosta_von_dem_Bussche-Haddenhausen
    literal_value: 1996
    literal_type: xsd:integer
  AddTriple (f27626c8-f846-46db-83ad-bb34751e59bc)
 Call ID: f27626c8-f846-46db-83ad-bb34751e59bc
  Args:
    source: Klaus_Felix_von_Amsberg
    relation: :hasMarriageYear
    target: Gosta_von_dem_Bussche-Haddenhausen
  AddLiteral (7c35e232-42e3-4ff2-ab69-5c60fdcb5afd)
 Call ID: 7c35e232-42e3-4ff2-ab69-5c60fdcb5afd
  Args:
    literal_type: xsd:integer
    literal_value: 1924
    source: Klaus_Felix_von_Amsberg
    relation: :hasMarriageYear
  AssignClass (61a5322c-d05e-40d2-8fa3-5aa3af0db195)
 Call ID: 61a5322c-d05e-40d2-8fa3-5aa3af0db195
  Args:
    type: :Man
    source: Georg_von_dem_Bussche-Haddenhausen
  AddLiteral (6d111964-87fd-42e1-b6a7-89a4e470287e)
 Call ID: 6d111964-87fd-42e1-b6a7-89a4e470287e
  Args:
    source: Georg_von_dem_Bussche-Haddenhausen
    literal_value: 1869
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (fb9d7ea3-9131-47ea-b731-ad1f9b188fdb)
 Call ID: fb9d7ea3-9131-47ea-b731-ad1f9b188fdb
  Args:
    source: Georg_von_dem_Bussche-Haddenhausen
    literal_value: 1923
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (e9e7f1b2-bb23-4b91-9286-6f703ef0ba4a)
 Call ID: e9e7f1b2-bb23-4b91-9286-6f703ef0ba4a
  Args:
    type: :Woman
    source: Gabriele_von_dem_Bussche-Ippenburg
  AddLiteral (d68e0012-be93-4ace-990f-ae10fb7d0ce1)
 Call ID: d68e0012-be93-4ace-990f-ae10fb7d0ce1
  Args:
    literal_value: 1877
    source: Gabriele_von_dem_Bussche-Ippenburg
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (70885cc1-14c0-41ed-9a8c-b058c94bd016)
 Call ID: 70885cc1-14c0-41ed-9a8c-b058c94bd016
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1973
    source: Gabriele_von_dem_Bussche-Ippenburg
  AddTriple (9735051c-87cc-4c62-b683-0400148a3c8c)
 Call ID: 9735051c-87cc-4c62-b683-0400148a3c8c
  Args:
    relation: :hasFather
    source: Gosta_von_dem_Bussche-Haddenhausen
    target: Georg_von_dem_Bussche-Haddenhausen
  AddTriple (ec92e9be-eaa4-42b8-93dd-7d07bfaa9009)
 Call ID: ec92e9be-eaa4-42b8-93dd-7d07bfaa9009
  Args:
    source: Gosta_von_dem_Bussche-Haddenhausen
    relation: :hasMother
    target: Gabriele_von_dem_Bussche-Ippenburg
  Finish (0d6bfa54-fba3-46db-8793-8a6255fa6152)
 Call ID: 0d6bfa54-fba3-46db-8793-8a6255fa6152
  Args: