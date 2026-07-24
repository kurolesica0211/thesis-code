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
Duchess Elisabeth of Mecklenburg-Schwerin (10 August 1869 – 3 September 1955) was a daughter of Frederick Francis II, Grand Duke of Mecklenburg by his third wife Princess Marie of Schwarzburg-Rudolstadt.
By her marriage to Frederick Augustus II, she became the consort of the last reigning Grand Duke of Oldenburg.
Family

Elisabeth was related to many of Europe's royal families.
She was the eldest child of Frederick Francis II, Grand Duke of Mecklenburg by his third wife, Princess Marie of Schwarzburg-Rudolstadt.
She was an older sister of Hendrik, Prince consort of the Netherlands, husband of Queen Wilhelmina of the Netherlands, making her an aunt of Queen Juliana of the Netherlands.
She was also a younger half-sister of Frederick Francis III, Grand Duke of Mecklenburg-Schwerin.
Through Frederick Francis, she was an aunt of Alexandrine, Queen of Denmark and Cecilie, German Crown Princess.
Elisabeth was also a half sister of Marie, Grand Duchess of Russia, who was the mother of Grand Duke Cyril Vladimirovich of Russia, the pretender to the Russian throne.
Her paternal grandparents were Paul Frederick, Grand Duke of Mecklenburg and Princess Alexandrine of Prussia.
Her maternal grandparents were Prince Adolph of Schwarzburg-Rudolstadt and Princess Mathilde of Schönburg-Waldenburg.
Marriage

On 24 October 1896, Elisabeth married Frederick Augustus, Hereditary Grand Duke of Oldenburg.
His first wife Elisabeth Anna had died the previous year, leaving only one surviving daughter: Duchess Sophia Charlotte of Oldenburg.
Frederick Augustus was thus in need of a male heir.
He succeeded as Grand Duke of Oldenburg in 1900, making Elisabeth Grand Duchess consort of Oldenburg.
They had five children:


Frederick was forced to abdicate his throne at the end of World War I, when the former Grand Duchy of the German Empire joined the post-war German Republic.
A year after his abdication, he asked the Oldenburg Diet for a yearly allowance of 150,000 marks, stating that his financial condition was "extremely precarious".
In 1931, Frederick died in Rastede.
Elisabeth died on 3 September 1955, having been widowed for 24 years.



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
  AssignClass (20583593-d04a-4887-bffa-5f08ec3ed17e)
 Call ID: 20583593-d04a-4887-bffa-5f08ec3ed17e
  Args:
    type: :Woman
    source: Elisabeth_of_Mecklenburg-Schwerin
  AssignClass (08555fd4-89b5-440b-872e-0723931d7198)
 Call ID: 08555fd4-89b5-440b-872e-0723931d7198
  Args:
    type: :Person
    source: Elisabeth_of_Mecklenburg-Schwerin
  AddLiteral (ff903608-bba9-4a0f-9e8d-934d647d1fbd)
 Call ID: ff903608-bba9-4a0f-9e8d-934d647d1fbd
  Args:
    literal_value: 1869
    source: Elisabeth_of_Mecklenburg-Schwerin
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (c25fc187-9495-4c06-8d34-53ca13d4762c)
 Call ID: c25fc187-9495-4c06-8d34-53ca13d4762c
  Args:
    relation: :hasDeathYear
    source: Elisabeth_of_Mecklenburg-Schwerin
    literal_type: xsd:integer
    literal_value: 1955
  AssignClass (5e3c5262-d9ae-43ef-9601-bfeee0615ddf)
 Call ID: 5e3c5262-d9ae-43ef-9601-bfeee0615ddf
  Args:
    type: :Man
    source: Frederick_Francis_II_of_Mecklenburg
  AssignClass (685f8c17-718e-453f-a480-261624119344)
 Call ID: 685f8c17-718e-453f-a480-261624119344
  Args:
    type: :Ancestor
    source: Frederick_Francis_II_of_Mecklenburg
  AssignClass (00f8dc2d-36c1-4bcd-913f-211b3ccaf27f)
 Call ID: 00f8dc2d-36c1-4bcd-913f-211b3ccaf27f
  Args:
    type: :Woman
    source: Marie_of_Schwarzburg-Rudolstadt
  AssignClass (4afee67a-379e-4332-b6c9-ebe25077481b)
 Call ID: 4afee67a-379e-4332-b6c9-ebe25077481b
  Args:
    type: :Ancestor
    source: Marie_of_Schwarzburg-Rudolstadt
  AddTriple (ddf9a3fb-1f8d-40a0-91f6-e2b53ca04dfb)
 Call ID: ddf9a3fb-1f8d-40a0-91f6-e2b53ca04dfb
  Args:
    target: Frederick_Francis_II_of_Mecklenburg
    source: Elisabeth_of_Mecklenburg-Schwerin
    relation: :hasFather
  AddTriple (6d66e02e-94f0-44c0-982c-6ab7dfa2443c)
 Call ID: 6d66e02e-94f0-44c0-982c-6ab7dfa2443c
  Args:
    source: Elisabeth_of_Mecklenburg-Schwerin
    target: Marie_of_Schwarzburg-Rudolstadt
    relation: :hasMother
  AssignClass (0fcda7fd-ca8a-44ba-8c2d-a296fbf34695)
 Call ID: 0fcda7fd-ca8a-44ba-8c2d-a296fbf34695
  Args:
    type: :Man
    source: Frederick_Augustus_II_of_Oldenburg
  AssignClass (ffc0478c-d58c-4788-a5af-6ec114b6027a)
 Call ID: ffc0478c-d58c-4788-a5af-6ec114b6027a
  Args:
    type: :Person
    source: Frederick_Augustus_II_of_Oldenburg
  AddLiteral (e0c2bd93-fc2f-4adc-bbf0-f1009c80155d)
 Call ID: e0c2bd93-fc2f-4adc-bbf0-f1009c80155d
  Args:
    literal_value: 1896
    relation: :hasMarriageYear
    source: Elisabeth_of_Mecklenburg-Schwerin
    literal_type: xsd:integer
  AddTriple (91d06210-2d76-43fc-9f40-0e5e7829dd20)
 Call ID: 91d06210-2d76-43fc-9f40-0e5e7829dd20
  Args:
    relation: :hasRelation
    target: Frederick_Augustus_II_of_Oldenburg
    source: Elisabeth_of_Mecklenburg-Schwerin
  AssignClass (90fa5faa-30ae-4ff8-8f6d-6fe9b9eb6756)
 Call ID: 90fa5faa-30ae-4ff8-8f6d-6fe9b9eb6756
  Args:
    type: :Man
    source: Hendrik_of_the_Netherlands
  AssignClass (5b7c5b90-17ac-4f60-910a-ff39a45389af)
 Call ID: 5b7c5b90-17ac-4f60-910a-ff39a45389af
  Args:
    type: :Person
    source: Hendrik_of_the_Netherlands
  AddTriple (409757e7-fd69-4b41-943e-11d29424dcdf)
 Call ID: 409757e7-fd69-4b41-943e-11d29424dcdf
  Args:
    relation: :isSiblingOf
    source: Elisabeth_of_Mecklenburg-Schwerin
    target: Hendrik_of_the_Netherlands
  AssignClass (902c4e70-7a30-41b7-8cf9-626af63483a4)
 Call ID: 902c4e70-7a30-41b7-8cf9-626af63483a4
  Args:
    type: :Woman
    source: Wilhelmina_of_the_Netherlands
  AssignClass (76cd2fe0-bb47-48d0-a92b-94f600b631bf)
 Call ID: 76cd2fe0-bb47-48d0-a92b-94f600b631bf
  Args:
    type: :Person
    source: Wilhelmina_of_the_Netherlands
  AddTriple (ea7100ec-8ea2-4762-8882-856dfece492b)
 Call ID: ea7100ec-8ea2-4762-8882-856dfece492b
  Args:
    target: Wilhelmina_of_the_Netherlands
    source: Hendrik_of_the_Netherlands
    relation: :hasRelation
  AssignClass (ab609750-3ec6-4ee4-9494-2c1860bbd4ec)
 Call ID: ab609750-3ec6-4ee4-9494-2c1860bbd4ec
  Args:
    source: Juliana_of_the_Netherlands
    type: :Woman
  AssignClass (efe0e8d1-01e4-4df6-b68e-454eeb8785c4)
 Call ID: efe0e8d1-01e4-4df6-b68e-454eeb8785c4
  Args:
    type: :Person
    source: Juliana_of_the_Netherlands
  AddTriple (8a6582a5-7cad-401a-a50e-93b0f2afad0b)
 Call ID: 8a6582a5-7cad-401a-a50e-93b0f2afad0b
  Args:
    relation: :isAuntOf
    source: Elisabeth_of_Mecklenburg-Schwerin
    target: Juliana_of_the_Netherlands
  AssignClass (35393e54-824e-4eee-a54e-61d7dda41dad)
 Call ID: 35393e54-824e-4eee-a54e-61d7dda41dad
  Args:
    type: :Man
    source: Frederick_Francis_III_of_Mecklenburg-Schwerin
  AssignClass (9673d769-6d77-4616-aca9-45aa1b59ade8)
 Call ID: 9673d769-6d77-4616-aca9-45aa1b59ade8
  Args:
    type: :Person
    source: Frederick_Francis_III_of_Mecklenburg-Schwerin
  AddTriple (2d6b3e16-c43b-4ac5-bb1b-1efeca3acab3)
 Call ID: 2d6b3e16-c43b-4ac5-bb1b-1efeca3acab3
  Args:
    relation: :isSiblingOf
    target: Frederick_Francis_III_of_Mecklenburg-Schwerin
    source: Elisabeth_of_Mecklenburg-Schwerin
  AssignClass (cc40dc8a-47d4-4795-aabb-ce8f0486b4b2)
 Call ID: cc40dc8a-47d4-4795-aabb-ce8f0486b4b2
  Args:
    type: :Woman
    source: Alexandrine_of_Denmark
  AssignClass (1df847cb-1ef5-4b51-b836-5f1444fbd683)
 Call ID: 1df847cb-1ef5-4b51-b836-5f1444fbd683
  Args:
    source: Alexandrine_of_Denmark
    type: :Person
  AssignClass (1359850b-9dcb-4375-87cf-d93ee150783d)
 Call ID: 1359850b-9dcb-4375-87cf-d93ee150783d
  Args:
    source: Cecilie_of_Germany
    type: :Woman
  AssignClass (3fa4256c-223b-4f0f-9bbe-4c0e1a236cf7)
 Call ID: 3fa4256c-223b-4f0f-9bbe-4c0e1a236cf7
  Args:
    type: :Person
    source: Cecilie_of_Germany
  AddTriple (1d8cbff9-b301-4b1d-887c-eabc406ceca3)
 Call ID: 1d8cbff9-b301-4b1d-887c-eabc406ceca3
  Args:
    target: Alexandrine_of_Denmark
    source: Elisabeth_of_Mecklenburg-Schwerin
    relation: :isAuntOf
  AddTriple (811de51e-ac12-4e10-8dc1-e64dd8dfcdee)
 Call ID: 811de51e-ac12-4e10-8dc1-e64dd8dfcdee
  Args:
    relation: :isAuntOf
    source: Elisabeth_of_Mecklenburg-Schwerin
    target: Cecilie_of_Germany
  AssignClass (ec483151-5a3c-48f9-b51b-794c07b32eb9)
 Call ID: ec483151-5a3c-48f9-b51b-794c07b32eb9
  Args:
    source: Marie_of_Russia
    type: :Woman
  AssignClass (b832c2e5-7098-4f04-a584-5522d5621254)
 Call ID: b832c2e5-7098-4f04-a584-5522d5621254
  Args:
    type: :Person
    source: Marie_of_Russia
  AddTriple (ed4dc9ad-9252-4a45-b365-3ce7ebc1d9e0)
 Call ID: ed4dc9ad-9252-4a45-b365-3ce7ebc1d9e0
  Args:
    source: Elisabeth_of_Mecklenburg-Schwerin
    target: Marie_of_Russia
    relation: :isSiblingOf
  AssignClass (4dfb6252-a0db-4d3b-aab6-5632766deed7)
 Call ID: 4dfb6252-a0db-4d3b-aab6-5632766deed7
  Args:
    source: Cyril_Vladimirovich_of_Russia
    type: :Man
  AssignClass (71d2e2f9-99a1-4100-b47d-71ea05317fb2)
 Call ID: 71d2e2f9-99a1-4100-b47d-71ea05317fb2
  Args:
    source: Cyril_Vladimirovich_of_Russia
    type: :Person
  AddTriple (68dcf912-f358-4190-bcda-eff1cf623604)
 Call ID: 68dcf912-f358-4190-bcda-eff1cf623604
  Args:
    relation: :hasMother
    target: Marie_of_Russia
    source: Cyril_Vladimirovich_of_Russia
  AssignClass (d33b3fa8-ca66-43a7-a5a9-a5efbff30002)
 Call ID: d33b3fa8-ca66-43a7-a5a9-a5efbff30002
  Args:
    type: :Man
    source: Paul_Frederick_of_Mecklenburg
  AssignClass (6926ccf2-d401-484f-b2e4-20a546cec44f)
 Call ID: 6926ccf2-d401-484f-b2e4-20a546cec44f
  Args:
    source: Paul_Frederick_of_Mecklenburg
    type: :Ancestor
  AssignClass (7e82d8b7-2e96-407d-a30e-cd1975bea90c)
 Call ID: 7e82d8b7-2e96-407d-a30e-cd1975bea90c
  Args:
    type: :Woman
    source: Alexandrine_of_Prussia
  AssignClass (19084566-4d87-4f88-b882-5aeda6591e56)
 Call ID: 19084566-4d87-4f88-b882-5aeda6591e56
  Args:
    type: :Ancestor
    source: Alexandrine_of_Prussia
  AddTriple (dc654a92-4af2-4185-a67d-356d197f5103)
 Call ID: dc654a92-4af2-4185-a67d-356d197f5103
  Args:
    target: Paul_Frederick_of_Mecklenburg
    source: Frederick_Francis_II_of_Mecklenburg
    relation: :hasFather
  AddTriple (890d84cc-3d76-4d28-9c7a-cc6d34dae209)
 Call ID: 890d84cc-3d76-4d28-9c7a-cc6d34dae209
  Args:
    relation: :hasMother
    target: Alexandrine_of_Prussia
    source: Frederick_Francis_II_of_Mecklenburg
  AssignClass (06818ffe-ee17-4202-b50d-a9c4d31034c3)
 Call ID: 06818ffe-ee17-4202-b50d-a9c4d31034c3
  Args:
    source: Adolph_of_Schwarzburg-Rudolstadt
    type: :Man
  AssignClass (e02a2168-df12-4e23-98aa-aa7548ed8429)
 Call ID: e02a2168-df12-4e23-98aa-aa7548ed8429
  Args:
    type: :Ancestor
    source: Adolph_of_Schwarzburg-Rudolstadt
  AssignClass (b4ca0aa8-44e7-4472-b691-aee8bdd7e4ed)
 Call ID: b4ca0aa8-44e7-4472-b691-aee8bdd7e4ed
  Args:
    type: :Woman
    source: Mathilde_of_Schönburg-Waldenburg
  AssignClass (f286aa80-665e-417c-a2e9-7d61695adaa2)
 Call ID: f286aa80-665e-417c-a2e9-7d61695adaa2
  Args:
    type: :Ancestor
    source: Mathilde_of_Schönburg-Waldenburg
  AddTriple (9df6f382-bd55-464b-8af5-8978435d28b1)
 Call ID: 9df6f382-bd55-464b-8af5-8978435d28b1
  Args:
    relation: :hasFather
    source: Marie_of_Schwarzburg-Rudolstadt
    target: Adolph_of_Schwarzburg-Rudolstadt
  AddTriple (8475e850-c8e0-4450-8467-ba576e02f231)
 Call ID: 8475e850-c8e0-4450-8467-ba576e02f231
  Args:
    source: Marie_of_Schwarzburg-Rudolstadt
    target: Mathilde_of_Schönburg-Waldenburg
    relation: :hasMother
  AssignClass (542f14d0-310b-464b-908d-7eeac6199dfb)
 Call ID: 542f14d0-310b-464b-908d-7eeac6199dfb
  Args:
    source: Elisabeth_Anna_of_Oldenburg
    type: :Woman
  AssignClass (1df515db-0893-4a3e-9e11-796810d66c7a)
 Call ID: 1df515db-0893-4a3e-9e11-796810d66c7a
  Args:
    type: :Person
    source: Elisabeth_Anna_of_Oldenburg
  AddTriple (5f2a0f68-cd02-45a2-82b7-3d0e434b2b59)
 Call ID: 5f2a0f68-cd02-45a2-82b7-3d0e434b2b59
  Args:
    relation: :hasRelation
    target: Elisabeth_Anna_of_Oldenburg
    source: Frederick_Augustus_II_of_Oldenburg
  AssignClass (582448f0-e8a9-40d1-9de3-69839becb8e3)
 Call ID: 582448f0-e8a9-40d1-9de3-69839becb8e3
  Args:
    source: Sophia_Charlotte_of_Oldenburg
    type: :Woman
  AssignClass (d123c518-1efb-4bb0-ba88-099c4d36f7f4)
 Call ID: d123c518-1efb-4bb0-ba88-099c4d36f7f4
  Args:
    type: :Person
    source: Sophia_Charlotte_of_Oldenburg
  AddTriple (43c8c031-ae65-4d20-a6b8-ad7b69ef4962)
 Call ID: 43c8c031-ae65-4d20-a6b8-ad7b69ef4962
  Args:
    target: Elisabeth_Anna_of_Oldenburg
    source: Sophia_Charlotte_of_Oldenburg
    relation: :hasMother
  AddTriple (b6c4fe44-13ec-479b-bfde-580c73091cfe)
 Call ID: b6c4fe44-13ec-479b-bfde-580c73091cfe
  Args:
    relation: :hasFather
    target: Frederick_Augustus_II_of_Oldenburg
    source: Sophia_Charlotte_of_Oldenburg
  Finish (0918c090-e64c-4604-b42c-c7c1b1520b3f)
 Call ID: 0918c090-e64c-4604-b42c-c7c1b1520b3f
  Args: