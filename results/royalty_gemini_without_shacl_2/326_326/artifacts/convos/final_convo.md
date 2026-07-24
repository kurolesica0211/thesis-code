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
Henri d'Orléans (Henri Robert Ferdinand Marie d'Orléans; 5 July 1908 – 19 June 1999), was the Orléanist pretender to the defunct throne of France as Henry VI from 1940 until his death in 1999.
Henri was the direct descendant of Philippe I, Duke of Orléans, son of Louis XIII.
He was also a descendant of Louis XIV through a female line, from his legitimized daughter Françoise Marie de Bourbon, as well as the great-great-grandson, by four different lines of descent, of Louis Philippe I.
The son of Jean, Duke of Guise, Henri was forbidden to enter France for much of his life.
Henri worked to restore the French monarchy in a parliamentary form, and discussed the topic with Charles de Gaulle.
Upon his death in 1999, his son Henri succeeded him as Head of the House of Orléans.
Here, Henri rose at 4 am daily, accompanying his father to oversee livestock management and crop production on their scattered lands, later in the day being tutored by European governesses and his mother: He acquired fluency in French, Arabic, English, German, Italian and Spanish.
Being rebuffed by France, Belgium and the United Kingdom, Prince Jean finally took his family back to Morocco and farming.
In 1921, Henri's governesses were replaced with a series of preceptors, all coming from France.
In 1923, the abbé Thomas took over Henri's instruction and, being less traditional in his approach, awakened in his charge a hitherto undetected thirst for knowledge.
Using the wedding of the prince's sister that year in France as an opportunity, Thomas obtained permission to take Henri to the Parisian banlieues of Meudon and Issy-les-Moulineaux, then working class slums in which the abbé would volunteer to serve the needy daily, bringing Henri into close contact with day laborers.
He would later write that this wretched urban experience profoundly affected his future political outlook and sense of justice, contrasting unfavourably with the deprivation to which he was accustomed in Morocco where, he observed, the poor were at least able to enjoy fresh air, space and sunlight while surrounded by relatives and neighbors who shared a near universal poverty, compared to the depressing grime, crowded conditions and anonymity in which Parisian workers toiled amidst extremes of wealth and deprivation.
After a year Thomas, whose health suffered in Morocco, was replaced as Henri's preceptor by abbé Dartein, who accompanied the family to France in 1924, preparing the prince for his collegiate matriculation while they occupied an apartment near his parents in Paris.
Henri began a two-year study of mathematics and the sciences at the Catholic University of Louvain in 1924, studying the law for the two years following.
From across the border in France came scholars and veterans of renown to coach Henri for his future role as a royalist leader, including jurist Ernest Perrot, military strategist Général Henri de Gondrecourt and the diplomat Charles Benoist, a member of the Académie des Sciences Morales et Politiques who would serve as his advisor from 1930.
Dauphin in pretence

In 1926, Henri became the Dauphin of France in pretence when his father became the Orléanist claimant to the defunct throne upon the death of his maternal uncle, Philippe, Duke of Orleans.
In 1939, after being refused admission to both the French and the British armed forces, Henri was allowed to join the French Foreign Legion.
Orléanist pretender

World War II

Henri became pretender to the defunct French throne on 25 August 1940 when his father died.
Henri was a "gentlemen farmer" in Morocco in the course of 1942.
In mid-November 1942, after Admiral François Darlan's armistice with the Allied invaders of North Africa, Vichy intelligence official Henri d'Astier de la Vigerie attempted to promote a royalist coup (d'Astier had previously conspired with the Allies to aid the invasion).
He proposed that Henri would appear to head a French government composed of all political tendencies, and maintain "neutrality until the day comes when the French nation can freely decide for itself."
Ridgeway was taken aback by the proposal, but was unaware that d'Astier's colleagues, Abbé Cordier and Master-Sergeant Sabatier (a French instructor at an OSS-SOE camp in Algiers), had secretly brought Henri from Morocco to d'Astier's apartment in Algiers.
Post war

In 1947, Henri and his family took up residence at the Quinta do Anjinho, an estate in Sintra, on the Portuguese Riviera.
In 1950, after the law of exile was rescinded, Henri returned to France.
During his tenure as pretender to the defunct throne, Henri used the majority of his family's great wealth, selling off family jewels, paintings, furniture and properties to support his political cause and large family, as well as establishments in Belgium, North Africa, Brazil, Portugal and France.
Political activity

Unlike his father, Henri devoted his life to politics.
During World War II, Henri was initially sympathetic to Vichy France.
His opinions on the government changed over time, and he contacted Prime Minister Pierre Laval.
Laval offered Henri the unglamorous position of Minister of Food, which he declined.
In Algeria, Henri attempted to convince the French military governor not to oppose an Anglo-American military landing.
Henri had correctly predicted such a thing occurring, but at the time he was laughed at by the officers.
Henri also tried to mediate between Charles de Gaulle and Henri Giraud, when the two men were competing for control of Free France.
Between 1940 and 1941, the Gaullist camp offered Henri an invitation to go to London, which he declined.
Henri feared that if he accepted the offer, he would have become an émigré, like the Bourbons who returned to France after Napoleon's defeat.
Henri was staunchly opposed to the idea of siding with one political party, wishing instead to pursue a path of unity and not contribute to France's "infernal divisiveness."
"


In 1948, Henri began publishing a monthly bulletin, which soon possessed 30,000 subscribers.
In 1950, the French Parliament abrogated the Law of Exile, permitting Henri to return.
So we have to make do with Henri, who strikes a royal enough pose, I guess.
In 1954, Henri met Charles de Gaulle and continued their relationship through correspondence.
In 1958, Henri gave his support to de Gaulle, who was called back from his self-imposed exile to save the French Republic from insurrection in Paris.
Thereafter, Henri became a frequent visitor to the Élysée Palace, where de Gaulle waited for Henri "by the staircase or outside, reserved a special armchair for him and lit his cigarette."
There, they frequently discussed French history together, with Henri noting that de Gaulle loved to pronounce the word 'king'.
In 1960, de Gaulle told Henri that "Monseigneur, I believe deeply in the value of the monarchy, and I am certain as well that this regime is the one best suited to our poor country."
The following year, de Gaulle dispatched Henri on a tour to Libya, Ethiopia, Iran, and Lebanon, with the purpose of explaining France's Algeria policy, serving as de Gaulle's special representative, or "pro-consul."
During this time, Henri befriended Hassan II of Morocco and Habib Bourguiba.
In 1962, de Gaulle informed Henri in strict confidence that he had arranged the French presidential election so that the head of the royal house could succeed him as president of the Republic.
However, by 1964, de Gaulle changed his mind and told Henri of his decision to run for re-election, which he won.
By 1968, Henri ceased publication of his paper over his increasing disagreements with the Gaullists.
The Countess of Paris remarked that "Under de Gaulle, Henri came two fingers close to becoming king.
"


Following de Gaulle's death in 1970, his son Philippe de Gaulle told Henri, "Monseigneur, my father often told me that if circumstances had been different, he would have been happy to be your faithful and loyal servant."
In 1979, Henri published his book Mémoires d'exil et de combats, which revealed to the public that de Gaulle had asked Henri to prepare himself for the 1965 presidential elections in France.
In a latter interview, Henri stated "At all times de Gaulle desired restoration, I am convinced of it.
However, Henri also noted that "It was difficult to get anywhere without de Gaulle, He agreed to favor my ascension to the highest point, but he didn't understand that it was necessary to give me the means of getting there.
"


Henri stated that he believes de Gaulle never forgave him for refusing to join the Free French in London, and also noted that "De Gaulle was not my friend...De Gaulle and I shared some common ideals and I agreed with him on the essentials of his approach to politics...
"


In 1988, Henri produced a scandal among his monarchist supporters when he supported the re-election of François Mitterrand, a socialist.
Political beliefs

In his college years, Henri spent many nights listening to the French monarchist writer Charles Maurras.
But during his adult life, Henri considered himself a centrist and never allied with any political party.
On Action Française, Henri stated that it had many talented leaders, but he ultimately regarded it as "a Rightist party with extreme Right sympathies."
In Henri's view, "no one should be in a position to claim a monopoly on the monarchist idea.
"


Henri befriended politicians on both the left and right, and declined to run for Parliament, despite de Gaulle's suggestion that he should do so.
Some rightist critics of Henri regarded him as "the Crown Prince of the Republic" or "a dyed-in-the-wool socialist, if not a Jacobin."
"


Henri was a critic of primogeniture and favored elective monarchy over hereditary.
Marriage and family life

On 8 April 1931, he married Princess Isabelle of Orléans-Braganza.
The wedding was celebrated in Palermo Cathedral in Sicily, the same church where their common ancestors, Louis Philippe of France and his Queen Maria Amalia, married in 1809.
In 1984, Henri declared that his son, Henri of Orléans, had lost his rights of inheritance because he had divorced his first wife and married a second time, outside of the Roman Catholic Church.
Henri gave his son the lesser-valued title comte de Mortain in place of comte de Clermont, and removed him from the line of succession.
After a couple of years, Henri reinstated his son with his previous titles, including reestablishing him as heir apparent and gave his new wife, Micaela Cousiño Quinones de Leon, the title "princesse de Joinville".
Henri deprived his sons Thibaut and Michel of their rights of succession to the defunct throne, because one married a commoner and the other wed a noblewoman whose father had been compromised during the Vichy regime.
His decision was later annulled by his son and successor, Henri.
Death

Henri, Count of Paris, died of prostate cancer at Cherisy, near Dreux, France, aged 90 on 19 June 1999.
Incidentally, his grandson Prince Eudes, Duke of Angoulême married on the very same day.
Issue

Henri, Count of Paris, and his wife Isabelle had eleven children:


Ancestry

References

Further reading

External links



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
  AssignClass (1f60c922-b9d6-422e-93b1-ce71b6bb9826)
 Call ID: 1f60c922-b9d6-422e-93b1-ce71b6bb9826
  Args:
    source: Henri_dOrleans
    type: :Man
  AssignClass (8e27202d-353a-4c85-9c74-4de567afd178)
 Call ID: 8e27202d-353a-4c85-9c74-4de567afd178
  Args:
    type: :Person
    source: Henri_dOrleans
  AddLiteral (bdfa4d04-7467-4995-a11c-f252f5a3532f)
 Call ID: bdfa4d04-7467-4995-a11c-f252f5a3532f
  Args:
    literal_type: xsd:integer
    literal_value: 1908
    source: Henri_dOrleans
    relation: :hasBirthYear
  AddLiteral (f5f45607-5ba7-401c-9b28-53923aa9742e)
 Call ID: f5f45607-5ba7-401c-9b28-53923aa9742e
  Args:
    relation: :hasDeathYear
    literal_value: 1999
    source: Henri_dOrleans
    literal_type: xsd:integer
  AssignClass (c0366ed9-4cb2-4015-a867-d5a34cfb39bd)
 Call ID: c0366ed9-4cb2-4015-a867-d5a34cfb39bd
  Args:
    source: Jean_Duke_of_Guise
    type: :Man
  AssignClass (2a074b1f-e00a-4576-a534-2da4755c4d98)
 Call ID: 2a074b1f-e00a-4576-a534-2da4755c4d98
  Args:
    type: :Person
    source: Jean_Duke_of_Guise
  AddTriple (f4429f39-f337-4d5f-a55f-689bb5f332b7)
 Call ID: f4429f39-f337-4d5f-a55f-689bb5f332b7
  Args:
    relation: :isSonOf
    source: Henri_dOrleans
    target: Jean_Duke_of_Guise
  AddTriple (820f575c-3158-4f24-ab69-3ccf8aa385cb)
 Call ID: 820f575c-3158-4f24-ab69-3ccf8aa385cb
  Args:
    target: Jean_Duke_of_Guise
    relation: :hasFather
    source: Henri_dOrleans
  AssignClass (47c714ca-0c62-472c-9766-28327942de4b)
 Call ID: 47c714ca-0c62-472c-9766-28327942de4b
  Args:
    source: Henri_the_son
    type: :Man
  AssignClass (6bad3054-a395-4037-b201-00114398633f)
 Call ID: 6bad3054-a395-4037-b201-00114398633f
  Args:
    source: Henri_the_son
    type: :Person
  AddTriple (8907ed39-0944-43ed-b40c-b67d0febc292)
 Call ID: 8907ed39-0944-43ed-b40c-b67d0febc292
  Args:
    target: Henri_dOrleans
    relation: :isSonOf
    source: Henri_the_son
  AddTriple (4a578c9e-e872-4ff5-98b5-34055126f4ab)
 Call ID: 4a578c9e-e872-4ff5-98b5-34055126f4ab
  Args:
    target: Henri_dOrleans
    source: Henri_the_son
    relation: :hasFather
  AssignClass (921270e9-d6c1-46d5-9ff9-c9f11320de57)
 Call ID: 921270e9-d6c1-46d5-9ff9-c9f11320de57
  Args:
    source: Isabelle_of_Orleans_Braganza
    type: :Woman
  AssignClass (1f132197-7992-4303-8046-0eb58b7ce04c)
 Call ID: 1f132197-7992-4303-8046-0eb58b7ce04c
  Args:
    source: Isabelle_of_Orleans_Braganza
    type: :Person
  AddTriple (797acb67-df42-43f6-9b0a-f24ff95dcfaf)
 Call ID: 797acb67-df42-43f6-9b0a-f24ff95dcfaf
  Args:
    target: Isabelle_of_Orleans_Braganza
    relation: :hasRelation
    source: Henri_dOrleans
  AddLiteral (26cf5839-f857-48de-80c7-caa6bee70da1)
 Call ID: 26cf5839-f857-48de-80c7-caa6bee70da1
  Args:
    source: Henri_dOrleans
    literal_value: 1931
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (a64217ac-7dff-46cc-961c-a2e8c2bf6fb3)
 Call ID: a64217ac-7dff-46cc-961c-a2e8c2bf6fb3
  Args:
    source: Philippe_Duke_of_Orleans
    type: :Man
  AssignClass (e6d58d79-da21-4127-b7cd-f64c7aca2ba7)
 Call ID: e6d58d79-da21-4127-b7cd-f64c7aca2ba7
  Args:
    source: Philippe_Duke_of_Orleans
    type: :Person
  AddTriple (2041c206-ef95-46c6-a3b1-4f5b1e6827b2)
 Call ID: 2041c206-ef95-46c6-a3b1-4f5b1e6827b2
  Args:
    relation: :hasBrother
    source: Jean_Duke_of_Guise
    target: Philippe_Duke_of_Orleans
  AddTriple (c91f6ba1-ac29-4fd3-8a93-cb9f8fd4721a)
 Call ID: c91f6ba1-ac29-4fd3-8a93-cb9f8fd4721a
  Args:
    target: Jean_Duke_of_Guise
    relation: :isBrotherOf
    source: Philippe_Duke_of_Orleans
  AssignClass (46cb9262-e51f-4cad-946e-6dd163cc2e72)
 Call ID: 46cb9262-e51f-4cad-946e-6dd163cc2e72
  Args:
    type: :Man
    source: Thibaut
  AssignClass (65a44c61-0068-4898-9bec-1000dd5a4b79)
 Call ID: 65a44c61-0068-4898-9bec-1000dd5a4b79
  Args:
    type: :Person
    source: Thibaut
  AddTriple (e8bba1ad-1773-493b-9a87-89f2c1bc2153)
 Call ID: e8bba1ad-1773-493b-9a87-89f2c1bc2153
  Args:
    target: Henri_dOrleans
    relation: :isSonOf
    source: Thibaut
  AssignClass (77283e74-23dd-428b-b225-341faf753070)
 Call ID: 77283e74-23dd-428b-b225-341faf753070
  Args:
    type: :Man
    source: Michel
  AssignClass (b615527f-ce40-4616-ac1b-b5989f9750a1)
 Call ID: b615527f-ce40-4616-ac1b-b5989f9750a1
  Args:
    source: Michel
    type: :Person
  AddTriple (58a28790-8c93-40c7-ba5a-4eaed1ee4bc8)
 Call ID: 58a28790-8c93-40c7-ba5a-4eaed1ee4bc8
  Args:
    source: Michel
    relation: :isSonOf
    target: Henri_dOrleans
  AssignClass (d372a4f1-d4a5-46f7-9ecb-0160865771c3)
 Call ID: d372a4f1-d4a5-46f7-9ecb-0160865771c3
  Args:
    type: :Man
    source: Eudes_Duke_of_Angouleme
  AssignClass (b6a3c2c4-a0d1-4bf8-a656-f5ef91ebd044)
 Call ID: b6a3c2c4-a0d1-4bf8-a656-f5ef91ebd044
  Args:
    source: Eudes_Duke_of_Angouleme
    type: :Person
  AddTriple (8d8e68be-59da-4fd0-837e-da318b759f17)
 Call ID: 8d8e68be-59da-4fd0-837e-da318b759f17
  Args:
    target: Henri_the_son
    source: Eudes_Duke_of_Angouleme
    relation: :isSonOf
  Finish (e2c20e1d-ff0d-43c0-9582-3963e38e803b)
 Call ID: e2c20e1d-ff0d-43c0-9582-3963e38e803b
  Args: