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
Archduhess Rosa Maria Antonie Roberta Josepha Anna Walburga Carmela Ignazia Rita de Cascia of Austria(German: Rosa Maria Antonie Roberta Josepha Anna Walburga Carmela Ignazia Rita de Cascia, Erzherzogin von Österreich; 22 September 1906 – 17 September 1983) was a member of the Tuscan branch of the House of Habsburg-Lorraine and an Archduchess of Austria and Princess of Bohemia, Hungary, and Tuscany by birth.
Through her marriage to Philipp Albrecht, Duke of Württemberg, Rosa was also a member of the House of Württemberg and Duchess consort of Württemberg.
Early life

Rosa was the fourth and youngest child of Archduke Peter Ferdinand, Prince of Tuscany, and his wife, Princess Maria Cristina of Bourbon-Two Sicilies.
Marriage and issue

Rosa married Philipp Albrecht, Duke of Württemberg, eldest child and son of Albrecht, Duke of Württemberg, and his wife, Archduchess Margarete Sophie of Austria, on 1 August 1928 in Friedrichshafen.
Rosa and Philipp Albrecht had two sons and four daughters:


Ancestry

References

Bibliography



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
  AssignClass (2301340b-5e8e-4ac1-aa0f-4ede8e66d77a)
 Call ID: 2301340b-5e8e-4ac1-aa0f-4ede8e66d77a
  Args:
    source: Rosa_Maria_Antonie_Roberta_Josepha_Anna_Walburga_Carmela_Ignazia_Rita_de_Cascia_of_Austria
    type: :Woman
  AssignClass (6ce1094e-17d6-47dd-b964-084ff4a8d956)
 Call ID: 6ce1094e-17d6-47dd-b964-084ff4a8d956
  Args:
    type: :Person
    source: Rosa_Maria_Antonie_Roberta_Josepha_Anna_Walburga_Carmela_Ignazia_Rita_de_Cascia_of_Austria
  AddLiteral (1d5cf607-6e53-479b-97e9-7c5a5b0e309c)
 Call ID: 1d5cf607-6e53-479b-97e9-7c5a5b0e309c
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Rosa_Maria_Antonie_Roberta_Josepha_Anna_Walburga_Carmela_Ignazia_Rita_de_Cascia_of_Austria
    literal_value: 1906
  AddLiteral (65997c12-9ff8-4c2e-87e6-01f8248b49b5)
 Call ID: 65997c12-9ff8-4c2e-87e6-01f8248b49b5
  Args:
    literal_value: 1983
    source: Rosa_Maria_Antonie_Roberta_Josepha_Anna_Walburga_Carmela_Ignazia_Rita_de_Cascia_of_Austria
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (92cb3385-43ef-4a4c-9776-7616e2115b68)
 Call ID: 92cb3385-43ef-4a4c-9776-7616e2115b68
  Args:
    type: :Man
    source: Peter_Ferdinand_of_Austria
  AssignClass (cc7b9015-55bf-48c2-bcec-1c0eb42262ed)
 Call ID: cc7b9015-55bf-48c2-bcec-1c0eb42262ed
  Args:
    type: :Person
    source: Peter_Ferdinand_of_Austria
  AssignClass (5cea1851-f05a-4b3d-9d5a-34744a69dbd2)
 Call ID: 5cea1851-f05a-4b3d-9d5a-34744a69dbd2
  Args:
    type: :Ancestor
    source: Peter_Ferdinand_of_Austria
  AssignClass (556f7917-11ff-4951-8da0-423ed264dcfa)
 Call ID: 556f7917-11ff-4951-8da0-423ed264dcfa
  Args:
    source: Maria_Cristina_of_Bourbon-Two_Sicilies
    type: :Woman
  AssignClass (ca59741b-4a58-4353-b7cd-1fd17aafcd2d)
 Call ID: ca59741b-4a58-4353-b7cd-1fd17aafcd2d
  Args:
    source: Maria_Cristina_of_Bourbon-Two_Sicilies
    type: :Person
  AssignClass (dd4593f6-74b5-41b6-81a5-5ec93de87e08)
 Call ID: dd4593f6-74b5-41b6-81a5-5ec93de87e08
  Args:
    source: Maria_Cristina_of_Bourbon-Two_Sicilies
    type: :Ancestor
  AddTriple (c582871a-c148-4f15-b8ac-70377656c4e5)
 Call ID: c582871a-c148-4f15-b8ac-70377656c4e5
  Args:
    source: Rosa_Maria_Antonie_Roberta_Josepha_Anna_Walburga_Carmela_Ignazia_Rita_de_Cascia_of_Austria
    relation: :hasFather
    target: Peter_Ferdinand_of_Austria
  AddTriple (7f29e758-4f7e-4374-996e-e77236b04504)
 Call ID: 7f29e758-4f7e-4374-996e-e77236b04504
  Args:
    relation: :hasMother
    target: Maria_Cristina_of_Bourbon-Two_Sicilies
    source: Rosa_Maria_Antonie_Roberta_Josepha_Anna_Walburga_Carmela_Ignazia_Rita_de_Cascia_of_Austria
  AssignClass (f0474b56-d206-487f-a6d8-b80c2d7a9e61)
 Call ID: f0474b56-d206-487f-a6d8-b80c2d7a9e61
  Args:
    type: :Man
    source: Philipp_Albrecht_of_Württemberg
  AssignClass (34c75386-fffb-4125-8e86-4f8afbb8e390)
 Call ID: 34c75386-fffb-4125-8e86-4f8afbb8e390
  Args:
    type: :Person
    source: Philipp_Albrecht_of_Württemberg
  AddLiteral (d84b3075-c82a-4845-8e3a-fff2db709ae4)
 Call ID: d84b3075-c82a-4845-8e3a-fff2db709ae4
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Rosa_Maria_Antonie_Roberta_Josepha_Anna_Walburga_Carmela_Ignazia_Rita_de_Cascia_of_Austria
    literal_value: 1928
  AddTriple (b4f4028f-4332-49f6-873d-ef56783581f8)
 Call ID: b4f4028f-4332-49f6-873d-ef56783581f8
  Args:
    target: Philipp_Albrecht_of_Württemberg
    relation: :hasRelation
    source: Rosa_Maria_Antonie_Roberta_Josepha_Anna_Walburga_Carmela_Ignazia_Rita_de_Cascia_of_Austria
  AssignClass (756650de-5d75-49c9-8cf7-c1e5732c8914)
 Call ID: 756650de-5d75-49c9-8cf7-c1e5732c8914
  Args:
    type: :Man
    source: Albrecht_of_Württemberg
  AssignClass (578e93be-3022-42a6-96b9-4c43b99c1d08)
 Call ID: 578e93be-3022-42a6-96b9-4c43b99c1d08
  Args:
    type: :Person
    source: Albrecht_of_Württemberg
  AssignClass (bb651cd0-d3ca-4630-9d92-dbb5d8204359)
 Call ID: bb651cd0-d3ca-4630-9d92-dbb5d8204359
  Args:
    type: :Ancestor
    source: Albrecht_of_Württemberg
  AssignClass (58b6290e-e1e3-4d84-b2c9-f68fa3669b15)
 Call ID: 58b6290e-e1e3-4d84-b2c9-f68fa3669b15
  Args:
    source: Margarete_Sophie_of_Austria
    type: :Woman
  AssignClass (1f10c0b4-337a-4750-8afb-24b65b86f332)
 Call ID: 1f10c0b4-337a-4750-8afb-24b65b86f332
  Args:
    source: Margarete_Sophie_of_Austria
    type: :Person
  AssignClass (682b2caf-c168-47cd-932a-d922aaff19bf)
 Call ID: 682b2caf-c168-47cd-932a-d922aaff19bf
  Args:
    type: :Ancestor
    source: Margarete_Sophie_of_Austria
  AddTriple (5861de53-a47b-4a85-bedf-f34e1a9bedf0)
 Call ID: 5861de53-a47b-4a85-bedf-f34e1a9bedf0
  Args:
    relation: :hasFather
    target: Albrecht_of_Württemberg
    source: Philipp_Albrecht_of_Württemberg
  AddTriple (229b2693-96cc-45f3-978c-0fc885dac47f)
 Call ID: 229b2693-96cc-45f3-978c-0fc885dac47f
  Args:
    relation: :hasMother
    target: Margarete_Sophie_of_Austria
    source: Philipp_Albrecht_of_Württemberg
  Finish (2b1a3a4e-e178-439c-b47e-fa2937196b0f)
 Call ID: 2b1a3a4e-e178-439c-b47e-fa2937196b0f
  Args: