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
  AssignClass (57406de7-df44-4241-95a1-8f0d0f941f2e)
 Call ID: 57406de7-df44-4241-95a1-8f0d0f941f2e
  Args:
    source: Rosa_Maria_Antonie_Roberta_Josepha_Anna_Walburga_Carmela_Ignazia_Rita_de_Cascia
    type: :Woman
  AssignClass (85178291-c083-4e5b-b87c-33e4055a57a8)
 Call ID: 85178291-c083-4e5b-b87c-33e4055a57a8
  Args:
    type: :Person
    source: Rosa_Maria_Antonie_Roberta_Josepha_Anna_Walburga_Carmela_Ignazia_Rita_de_Cascia
  AddLiteral (4e3e4afc-3fa3-4ff8-8f76-55659107bd2d)
 Call ID: 4e3e4afc-3fa3-4ff8-8f76-55659107bd2d
  Args:
    source: Rosa_Maria_Antonie_Roberta_Josepha_Anna_Walburga_Carmela_Ignazia_Rita_de_Cascia
    literal_value: 1906
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (fefd7b7e-2c17-4447-90d2-ff69bf196c0a)
 Call ID: fefd7b7e-2c17-4447-90d2-ff69bf196c0a
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1983
    source: Rosa_Maria_Antonie_Roberta_Josepha_Anna_Walburga_Carmela_Ignazia_Rita_de_Cascia
  AssignClass (f74a1d1a-5b54-4afb-b6ad-f9fbc96cb544)
 Call ID: f74a1d1a-5b54-4afb-b6ad-f9fbc96cb544
  Args:
    source: Peter_Ferdinand
    type: :Man
  AssignClass (bcf30d1b-0dd7-41b1-a03d-261f8c0363bf)
 Call ID: bcf30d1b-0dd7-41b1-a03d-261f8c0363bf
  Args:
    type: :Person
    source: Peter_Ferdinand
  AssignClass (ef21a730-54ec-4a18-8644-379a45887634)
 Call ID: ef21a730-54ec-4a18-8644-379a45887634
  Args:
    source: Peter_Ferdinand
    type: :Ancestor
  AssignClass (fb1d2a77-7861-4ec8-aed7-7c730aa9c775)
 Call ID: fb1d2a77-7861-4ec8-aed7-7c730aa9c775
  Args:
    source: Maria_Cristina_of_Bourbon-Two_Sicilies
    type: :Woman
  AssignClass (132ec9ea-cb74-48d7-af6a-36c7d8881229)
 Call ID: 132ec9ea-cb74-48d7-af6a-36c7d8881229
  Args:
    type: :Person
    source: Maria_Cristina_of_Bourbon-Two_Sicilies
  AssignClass (b7714d42-60c7-4339-8a01-2ad6b42005ce)
 Call ID: b7714d42-60c7-4339-8a01-2ad6b42005ce
  Args:
    source: Maria_Cristina_of_Bourbon-Two_Sicilies
    type: :Ancestor
  AddTriple (2602c727-0a58-4d3f-8596-3bab87236000)
 Call ID: 2602c727-0a58-4d3f-8596-3bab87236000
  Args:
    source: Rosa_Maria_Antonie_Roberta_Josepha_Anna_Walburga_Carmela_Ignazia_Rita_de_Cascia
    target: Peter_Ferdinand
    relation: :hasFather
  AddTriple (0632c80a-4989-4b20-a2d1-fb41c221f291)
 Call ID: 0632c80a-4989-4b20-a2d1-fb41c221f291
  Args:
    source: Rosa_Maria_Antonie_Roberta_Josepha_Anna_Walburga_Carmela_Ignazia_Rita_de_Cascia
    target: Maria_Cristina_of_Bourbon-Two_Sicilies
    relation: :hasMother
  AssignClass (0017f131-32d4-449b-9bf5-367e03f10428)
 Call ID: 0017f131-32d4-449b-9bf5-367e03f10428
  Args:
    source: Philipp_Albrecht_of_Wurttemberg
    type: :Man
  AssignClass (aea5a918-4266-4e8e-8c2c-3f3f6e3e5f5e)
 Call ID: aea5a918-4266-4e8e-8c2c-3f3f6e3e5f5e
  Args:
    type: :Person
    source: Philipp_Albrecht_of_Wurttemberg
  AddLiteral (0aa92e93-8c07-4b4d-aca1-a74f7e2517eb)
 Call ID: 0aa92e93-8c07-4b4d-aca1-a74f7e2517eb
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1928
    source: Rosa_Maria_Antonie_Roberta_Josepha_Anna_Walburga_Carmela_Ignazia_Rita_de_Cascia
  AddTriple (a9b56225-1cce-45fd-b9bd-aeb1eddec121)
 Call ID: a9b56225-1cce-45fd-b9bd-aeb1eddec121
  Args:
    relation: :hasRelation
    target: Philipp_Albrecht_of_Wurttemberg
    source: Rosa_Maria_Antonie_Roberta_Josepha_Anna_Walburga_Carmela_Ignazia_Rita_de_Cascia
  AssignClass (66610541-07ec-48a6-9f5d-42c87e4812f1)
 Call ID: 66610541-07ec-48a6-9f5d-42c87e4812f1
  Args:
    source: Albrecht_of_Wurttemberg
    type: :Man
  AssignClass (4d5b6546-f249-4b8e-a3e1-69a8569b50d7)
 Call ID: 4d5b6546-f249-4b8e-a3e1-69a8569b50d7
  Args:
    source: Albrecht_of_Wurttemberg
    type: :Person
  AssignClass (e057110c-f660-4375-b9ed-ccda05482227)
 Call ID: e057110c-f660-4375-b9ed-ccda05482227
  Args:
    type: :Ancestor
    source: Albrecht_of_Wurttemberg
  AssignClass (68bce253-18ff-46bb-b14b-88a1e68c1e30)
 Call ID: 68bce253-18ff-46bb-b14b-88a1e68c1e30
  Args:
    type: :Woman
    source: Margarete_Sophie_of_Austria
  AssignClass (a5708127-42f7-4346-8a25-8ba73fa434df)
 Call ID: a5708127-42f7-4346-8a25-8ba73fa434df
  Args:
    source: Margarete_Sophie_of_Austria
    type: :Person
  AssignClass (f0d8e17b-583a-491b-9569-ede3d5ae4eff)
 Call ID: f0d8e17b-583a-491b-9569-ede3d5ae4eff
  Args:
    source: Margarete_Sophie_of_Austria
    type: :Ancestor
  AddTriple (ccfd3188-df77-4444-b44c-85cf131b40be)
 Call ID: ccfd3188-df77-4444-b44c-85cf131b40be
  Args:
    source: Philipp_Albrecht_of_Wurttemberg
    relation: :hasFather
    target: Albrecht_of_Wurttemberg
  AddTriple (0ecc6c7d-b5f8-4e8c-9884-22b9b01dc8f9)
 Call ID: 0ecc6c7d-b5f8-4e8c-9884-22b9b01dc8f9
  Args:
    relation: :hasMother
    target: Margarete_Sophie_of_Austria
    source: Philipp_Albrecht_of_Wurttemberg
  Finish (1d1dd8f9-dd32-430c-955e-24bcbba1886b)
 Call ID: 1d1dd8f9-dd32-430c-955e-24bcbba1886b
  Args: